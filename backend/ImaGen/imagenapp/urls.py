from django.urls import path
from imagenapp import views


urlpatterns = [
    path('', views.index , name='home'),
    path('images/', views.resizeImage, name='images'),
]
