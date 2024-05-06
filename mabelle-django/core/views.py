from django.shortcuts import render
from django.http import JsonResponse
from .models import Reading
from api.iot_cloud_fetch import *
import asyncio
from core.utils import *
import onnx
import onnxruntime as ort

access_token = get_access_token()

async def data_util():
    data = await fetch_data(access_token)
    return data

def create_npk_object(request):
    # Fetch data asynchronously using sync_to_async
    data = asyncio.run(data_util())

    npk_t_h_values = {
        "Timestamp": 0,
        "Humidity": 0,
        "Nitrogen": 0,
        "Phosphorus": 0,
        "Potassium": 0,
        "Temperature": 0,
    }

    while not data:
        continue

    try:
        for obj in data:
            if(obj.name in npk_t_h_values.keys()):
                npk_t_h_values[obj.name] = obj.last_value

        # npk_t_h_values = [0 if x == 'N/A' else x for x in npk_t_h_values]
        
        # Create NPK object with the extracted attributes
        npk_obj = Reading.objects.create(
            timestamp = data[0].value_updated_at,
            humidity = npk_t_h_values['Humidity'],
            nitrogen_level = npk_t_h_values['Nitrogen'],
            phosphorus_level = npk_t_h_values['Phosphorus'],
            potassium_level = npk_t_h_values['Potassium'],
            temperature = npk_t_h_values['Temperature'],
        )

        return JsonResponse({'message': f'Objects created successfully {npk_obj}'}, status=200)
    except Exception as e:
        return JsonResponse({'message': f'No data available, {e}'}, status=404)


def run_inferrence(request):
    latest_reading = Reading.objects.latest('timestamp')

    ann_n = classify_nitrogen(latest_reading.nitrogen_level)
    ann_p = classify_phosphorus(latest_reading.phosphorus_level)
    ann_k = classify_potassium(latest_reading.nitrogen_level)
    ann_t = classify_temperature(latest_reading.temperature)
    ann_h = classify_humidity(latest_reading.humidity)
    ann_r = estimate_rain_intensity(ann_t, ann_h)

    test_data = [ann_n, ann_p, ann_k, ann_t, ann_h, ann_r]
    
    # Dummy data for testing purposes
    # test_data = [13, 13, 14, 1, 2, 0]
    # 9 0 3 0 5 0 1

    onnx_model_path = './static/weights/model_d2_b1.onnx'

    onnx_model = onnx.load(onnx_model_path)
    onnx.checker.check_model(onnx_model)

    # Load the ONNX model
    ort_session = ort.InferenceSession(onnx_model_path)

    # Extract input data
    x = np.array(test_data, dtype=np.float32)
    x = np.expand_dims(x, axis=0)  # Add batch dimension

    try: 
        outputs = ort_session.run(None, {'input': x})
        # Flatten the array and extract all values as rounded ints
        output_values = [int(round(value)) for sublist in outputs for arr in sublist for value in arr]
        to_return = [output_values[1], output_values[3], output_values[5], output_values[6]]

        # Send NPKW data to Arduino Cloud
        ids = load_npkw_ids()
        for i in range(len(ids)):
            post_data(access_token, ids[i], to_return[i])

        return JsonResponse({'message': f'Inferrence successful: {to_return}'}, status=200)
    except Exception as e:
        return JsonResponse({'message': f'An Exception has occured: {e}'}, status=404)