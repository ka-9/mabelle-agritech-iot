from django.shortcuts import render
from django.http import JsonResponse
from .models import NPKReading
from api.iot_cloud_fetch import get_access_token, fetch_data

access_token = get_access_token()

def create_npk_object(request):
    data = fetch_data(access_token)

    npk_values = []

    if data:
        for obj in data:
            npk_values.append(obj.last_value)
            
        # Create NPK object with the extracted attributes
        npk_obj = NPKReading.objects.create(
            timestamp = data[0].value_updated_at,
            nitrogen_level = npk_values[0],
            phosphorus_level = npk_values[1],
            potassium_level = npk_values[2]
        )

        print(npk_obj.timestamp)

        return JsonResponse({'message': 'NPK objects created successfully'}, status=200)
    else:
        return JsonResponse({'message': 'No data available'}, status=404)
