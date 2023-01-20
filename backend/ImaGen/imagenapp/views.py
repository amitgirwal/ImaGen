from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

import numpy as np
import cv2
import os
from django.core.files.storage import default_storage
from PIL import Image
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage

# Custom Import
from .models import Upload, ImageQuality
from .forms import UploadForm, ImageConvertForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            messages.success(request, "Image saved succesfully 📽️")
        else:
            messages.error(request, "Invalid Data Found 🙅")

    context = {
        'form': UploadForm(),
        'images': Upload.objects.all() 
    }
    return render(request, 'index.html', context)


def resizeImage(request):
    context = {}
    return render(request, 'index.html', context)


def imageDelete(request, pk):
    upload = get_object_or_404(Upload, id=pk)
    if upload:
        upload.delete()
        messages.success(request, "📽️ Image deleted succesfully")
    return redirect('home') 

def image_view(request, pk):
    image = get_object_or_404(Upload, id=pk)
    name = image.name
    return render(request, "index.html", locals())


def convertImage(image):
    pil_img = Image.open(image)
    cv_img = np.array(pil_img)
    action = 'png'
    
    # convert back to pil image
    im_pil = Image.fromarray(cv_img)

    # save
    buffer = BytesIO()
    im_pil.save(buffer, format=action)
    image_png = buffer.getvalue()
    return image_png


def get_filtered_image(image, action):
    #img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    filtered = None
    if action == 'NO_FILTER':
        filtered = image
    elif action == 'png':
         
         # percent of original size
        scale_percent = 220
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        
        # resize image
        filtered = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
         
    elif action == 'GRAYSCALE':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     
    return filtered


def convert_to_webp(filename, path="images/"):
    extension = filename.split('.')[-1]
    fname = filename.split('.')[0]
    img = Image.open(path + filename)

    if extension == "png":
        img.save((path+fname+".webp"), "webp", lossless=True)
    elif extension == "jpg" or extension == "jpeg":
        img.save((path+fname+".webp"), "webp", quality=85)



def imageConvert(request):
    if request.method=='POST':
        image = request.FILES['image']
        upload = Upload(
            name='image-name', 
            image=image, 
            action='png' 
            )


        filename = image.name
        fname = filename.split('.')[0]
        extension = filename.split('.')[-1]
        path = settings.MEDIA_URL
        

        img = Image.open(image)
        if extension == "png":
            img.save((image), "webp", lossless=True)
        elif extension == "jpg" or extension == "jpeg":
            img.save((image), "webp", quality=85)

         
        
   
        fs = FileSystemStorage()
        image_file = fs.save(str(img), ContentFile(img))
        uploaded_file_url = fs.url(image_file)

        return render(request, 'image-convert.html', {
            'uploaded_file_url': uploaded_file_url
        })
        
    return render(request, 'image-convert.html', {'form':ImageConvertForm()})

 
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File

def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image

 
def temp(request):
    uploaded_file_url = None
    if request.method=='POST':
        imgForm = ImageConvertForm(request.POST, request.FILES)
        if imgForm.is_valid():
            image = imgForm.save()
            messages.success(request, "Image saved sucessfully")
            uploaded_file_url = image.image.url
        else:
            messages.error(request, imgForm.errors)

    return render(request, 'temp.html', {'form':ImageConvertForm(), 'uploaded_file_url': uploaded_file_url})


import os

from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest, HttpResponseNotAllowed
 
 
 
from django.utils.decorators import method_decorator
from django.http import Http404
from django.conf import settings

 
import os
from PIL import Image, ImageFilter, ImageEnhance


# method used for sepia definition
def make_linear_ramp(white):
    ramp = []
    r, g, b = white
    for i in range(255):
        ramp.extend((r * i / 255, g * i / 255, b * i / 255))
    return ramp


class Applyeffects(object):
    def __init__(self, pilimage):
        self.pilimage = pilimage

    def effect(self, effect):
        filepath, ext = os.path.splitext(self.pilimage)
        edit_path = filepath + 'edited' + ext
        img = None
        if effect == 'brightness':
            img = Image.open(self.pilimage)
            enh = ImageEnhance.Brightness(img)
            img = enh.enhance(1.8)

        if effect == 'grayscale':

            img = Image.open(self.pilimage).convert('L')

        if effect == 'blackwhite':

            img = Image.open(self.pilimage).convert('1')

        if effect == 'sepia':

            serpia = make_linear_ramp((255, 240, 192))
            img = Image.open(self.pilimage).convert('L')
            img.putpalette(serpia)

        if effect == 'contrast':

            img = Image.open(self.pilimage)
            enh = ImageEnhance.Contrast(img)
            img = enh.enhance(2.0)

        # Filters here
        if effect == 'blur':

            img = Image.open(self.pilimage)
            img = img.filter(ImageFilter.BLUR)

        if effect == 'findedges':

            img = Image.open(self.pilimage)
            img = img.filter(ImageFilter.FIND_EDGES)

        if effect == 'bigenhance':

            img = Image.open(self.pilimage)
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        if effect == 'enhance':

            img = Image.open(self.pilimage)
            img = img.filter(ImageFilter.EDGE_ENHANCE)

        if effect == 'smooth':

            img = Image.open(self.pilimage)
            img = img.filter(ImageFilter.SMOOTH_MORE)

        if effect == 'emboss':

            img = Image.open(self.pilimage)
            img = img.filter(ImageFilter.EMBOSS)

        if effect == 'contour':

            img = Image.open(self.pilimage)
            img = img.filter(ImageFilter.CONTOUR)

        if effect == 'sharpen':

            img = Image.open(self.pilimage)
            img = img.filter(ImageFilter.SHARPEN)

        img.save(edit_path, format='PNG', quality=100)


def getImagePathUrlByFilesRequest(req_image):
    fs = FileSystemStorage()
    image_file = fs.save(str(req_image), ContentFile(req_image.read()))
    upload_url = fs.url(image_file)
    upload_path = fs.path(image_file)
    upload_name = str(image_file)
    return upload_url, upload_path, upload_name, image_file

def applyFilterSaveImage(upload_path, image_file, file_name):
    extension = 'jpg'
    img = Image.open(upload_path)
    # apply filter
    # img = img.filter(ImageFilter.EMBOSS)
    # save filter
    # img.save(upload_path, format='WEBP', quality=40)

    file_name, extension = getFileNameExt(upload_path)
    if extension == "png":
        img.save(file_name+'.webp', "webp", lossless=True)
    elif extension == "jpg" or extension == "jpeg":
        img.save(file_name+'.webp', format="webp", quality=85)

def printStar():
	print()
	print('#'*100)

def getFileNameExt(upload_name):
    file_name = upload_name.split('.')[0]
    extension = upload_name.split('.')[-1]
    return file_name, extension

class PillowImageView(TemplateView):
    def post(self, request, *args, **kwargs):
        printStar()    
        image = request.FILES['image']
        upload_url, upload_path, upload_name, image_file = getImagePathUrlByFilesRequest(image)
        
        file_name, extension = getFileNameExt(upload_name)
        applyFilterSaveImage(upload_path, image_file, file_name)
        print(upload_url, upload_path, image_file, upload_name)
        
        
        printStar()
        return HttpResponse("<h1>Done</h1>"+str(upload_url))


 