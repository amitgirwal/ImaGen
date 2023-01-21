from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# custom import
from .models import Upload, ImageConvert, ImageFilter
from .forms import UploadForm, ImageConvertForm, ImageFilterForm

# image utils
from .utils import getImagePathUrlByFilesRequest, convertAndSaveImage, getFileNameExt, printStar

# storage
from django.core.files.storage import FileSystemStorage

# settings
from django.conf import settings

def index(request):
    context = { 'form': UploadForm() }
    return render(request, 'index.html', context)

# def imageConvert(request):
#     uploaded_file_url = None
#     if request.method == 'POST':
#         printStar()    
#         image = request.FILES['image']
#         upload_url, upload_path, upload_name, image_file = getImagePathUrlByFilesRequest(image)
#         file_name, extension = getFileNameExt(upload_name)
#         applyFilterSaveImage(upload_path, image_file, file_name)
#         print(upload_url, upload_path, image_file, upload_name)
#         printStar()
#     context = {
#         'form': ImageConvertForm(),
#         'uploaded_file_url': uploaded_file_url
#     }
#     return render(request, 'image-convert.html', context)


def imageConvert(request):
    uploaded_file_url = None
    action = request.GET.get('action')
    if request.method == 'POST':
        printStar()    
        image = request.FILES['image']
        action = request.POST.get('convert')
        upload_url, upload_path, upload_name, image_file = getImagePathUrlByFilesRequest(image)
        file_name, extension = getFileNameExt(upload_name)
        file_name = convertAndSaveImage(upload_path, image_file, file_name, action)
        uploaded_file_url = settings.MEDIA_URL+file_name
        printStar()
    context = {
        'form': ImageConvertForm(),
        'uploaded_file_url': uploaded_file_url,
        'action': action
    }
    return render(request, 'image-convert.html', context)

# Image Filter
def imageFilter(request):
    uploaded_file_url = None
    action = request.GET.get('action')
    if request.method == 'POST':
        printStar()    
        image = request.FILES['image']
        action = request.POST.get('filter')
        upload_url, upload_path, upload_name, image_file = getImagePathUrlByFilesRequest(image)
        file_name, extension = getFileNameExt(upload_name)
        applyFilterSaveImage(upload_path, image_file, file_name, action)
        uploaded_file_url = upload_url
        print(upload_url, upload_path, image_file, upload_name)
        printStar()
    context = {
        'form': ImageFilterForm(),
        'uploaded_file_url': uploaded_file_url,
        'action': action
    }
    return render(request, 'image-filter.html', context)