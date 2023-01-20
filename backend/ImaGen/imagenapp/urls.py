from django.urls import path
from imagenapp import views


urlpatterns = [
    path('', views.index , name='home'),
    path('images/', views.resizeImage, name='images'),

    # path('images/<int:pk>/update/', views.imageUpdate, name='image_update'),
    path('images/<int:pk>/delete/', views.imageDelete, name='image_delete'),

    path("image/<int:pk>/", views.image_view, name="image_view"),
    

    
    path("image-convert/", views.imageConvert, name="image_convert"),
    
    path("temp/", views.temp, name="temp"),

     

    path("addeffects/", views.PillowImageView.as_view(), name="addeffects"),
    
]
