from django.urls import path
from imagenapp import views

app_name = 'imagenapp'

urlpatterns = [
    path('', views.index , name='home'),
    path('images', views.resizeImage, name='images'),
    path('temp', views.temp, name='temp')

    
]
