# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
import os
import requests
import json

url = 'http://localhost:8501/v1/models/my_model:predict'

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def predict_images(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # Save the uploaded image temporarily
        with open('temp_image.jpg', 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        image = cv2.imread('temp_image.jpg')
        image = cv2.resize(image, (224, 224))
        predictions = make_prediction(np.array([image]))
        if predictions[0][0] <0.5:
            pred = 1-predictions[0][0]
        else:
            pred = predictions[0][0]

        os.remove('temp_image.jpg')  # Remove the temporary image file

        return render(request, 'index.html', {'predicted_class': 'DOG' if predictions[0][0] > 0.5 else 'CAT', 'percentage': f'{pred*100:.5f}'})
    else:
        return render(request, 'index.html', {'error': 'Image upload failed'})

def make_prediction(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions

