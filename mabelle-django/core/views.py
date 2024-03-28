from django.shortcuts import render
from django.http import JsonResponse
from .models import NPKReading
from api.iot_cloud_fetch import get_access_token, fetch_data

access_token = get_access_token()

def create_npk_objects(request):
    data = fetch_data(access_token)

    npk_values = []

    if data:
        for obj in data:
            value_updated_at = obj.value_updated_at
            npk_values.append(obj.last_value)
            
        # Create NPK object with the extracted attributes
        npk_obj = NPKReading.objects.create(
            timestamp = value_updated_at,
            nitrogen_level = npk_values[0],
            phosphorus_level = npk_values[1],
            potassium_level = npk_values[2]
        )

        return JsonResponse({'message': 'NPK objects created successfully'}, status=200)
    else:
        return JsonResponse({'message': 'No data available'}, status=404)
