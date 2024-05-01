from django.shortcuts import render
from django.http import JsonResponse
from .models import Reading
from api.iot_cloud_fetch import get_access_token, fetch_data
import asyncio

access_token = get_access_token()

async def data_util():
    data = await fetch_data(access_token)
    return data

def create_npk_object(request):
    # Fetch data asynchronously using sync_to_async
    data = asyncio.run(data_util())

    npk_t_h_values = []

    if data:
        print(data)
        for obj in data:
            npk_t_h_values.append(obj.last_value)

        npk_t_h_values = [0 if x == 'N/A' else x for x in npk_t_h_values]
        
        # Create NPK object with the extracted attributes
        npk_obj = Reading.objects.create(
            timestamp = data[0].value_updated_at,
            humidity = npk_t_h_values[0],
            nitrogen_level = npk_t_h_values[1],
            phosphorus_level = npk_t_h_values[2],
            potassium_level = npk_t_h_values[3],
            temperature = npk_t_h_values[5],
        )

        return JsonResponse({'message': f'Objects created successfully {npk_obj}'}, status=200)
    else:
        return JsonResponse({'message': 'No data available'}, status=404)
