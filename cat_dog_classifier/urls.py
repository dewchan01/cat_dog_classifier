from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_images, name='predict_images'),
]