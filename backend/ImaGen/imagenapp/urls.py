from django.urls import path
from imagenapp import views


urlpatterns = [
    # path('', views.index , name='home'),
    # path('images/', views.resizeImage, name='images'),
    # # path('images/<int:pk>/update/', views.imageUpdate, name='image_update'),
    # path('images/<int:pk>/delete/', views.imageDelete, name='image_delete'),
    # path("image/<int:pk>/", views.image_view, name="image_view"),
    # # path("image-convert/", views.imageConvert, name="image_convert"),
    # path("image-convert", views.imageConvert, name="image_convert"),
    # path("temp/", views.temp, name="temp"),
    # path("addeffects/", views.PillowImageView.as_view(), name="addeffects"),
    
    path('', views.index , name='home'),
    path('image-convert', views.imageConvert , name='image_convert'),
    path('image-filter', views.imageFilter , name='image_filter'),
    path('image-quality', views.imageQuality , name='image_quality'),
    path('qr-code-gen', views.qrGen , name='qr_gen'),
    path('image-rotate', views.imageRotate , name='image_rotate'),
    path('image-pdf', views.imageToPDF , name='image_pdf'),

    path("tempa", views.tempa, name="tempa"),
    path("tempajax", views.tempAjax, name="temp_ajax"),


]
