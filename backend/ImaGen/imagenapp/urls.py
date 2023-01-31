from django.urls import path
from imagenapp import views


urlpatterns = [

    path('', views.index, name='home'),
    path('qr-code-gen', views.qrGen, name='qr_gen'),
    path('image-pdf', views.imageToPDF, name='image_pdf'),
    path('colorize-filter', views.colorizeFilter, name='colorize_filter'),
    path('image-convert', views.imageConvert, name='image_convert'),
    path('image-quality', views.imageQuality, name='image_quality'),
    path('image-rotate', views.imageRotate, name='image_rotate'),
    path('image-flip', views.imageFlip, name='image_flip'),


    # path('', views.index , name='home'),
    # path('images/', views.resizeImage, name='images'),
    # # path('images/<int:pk>/update/', views.imageUpdate, name='image_update'),
    # path('images/<int:pk>/delete/', views.imageDelete, name='image_delete'),
    # path("image/<int:pk>/", views.image_view, name="image_view"),
    # # path("image-convert/", views.imageConvert, name="image_convert"),
    # path("image-convert", views.imageConvert, name="image_convert"),
    # path("temp/", views.temp, name="temp"),
    # path("addeffects/", views.PillowImageView.as_view(), name="addeffects"),
    
    path('image-filter', views.imageFilter, name='image_filter'),
    path("tempa", views.tempa, name="tempa"),
    path("tempajax", views.tempAjax, name="temp_ajax"),

]
