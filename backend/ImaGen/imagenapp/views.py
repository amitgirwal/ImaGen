from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# custom import
from .models import Upload, ImageConvert, ImageFilter
from .forms import UploadForm, ImageConvertForm, ImageFilterForm, ImageQualityForm, ImageToPDFForm, ImageRotateForm

# image utils
from .utils import getImagePathUrlByFilesRequest, convertAndSaveImage, getFileNameExt, printStar, reduceQualitySaveImage, filterSaveImage, imgToPDF

# storage
from django.core.files.storage import FileSystemStorage

# settings
from django.conf import settings


from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from django.http import FileResponse

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
        filterSaveImage(upload_path, image_file, file_name, action)
        uploaded_file_url = upload_url
        print(upload_url, upload_path, image_file, upload_name)
        printStar()
    context = {
        'form': ImageFilterForm(),
        'uploaded_file_url': uploaded_file_url,
        'action': action
    }
    return render(request, 'image-filter.html', context)


# Image Compress
def imageQuality(request):
    uploaded_file_url = None
    action = request.GET.get('action')
    if request.method == 'POST':
        printStar()    
        image = request.FILES['image']
        action = request.POST.get('quality')
        upload_url, upload_path, upload_name, image_file = getImagePathUrlByFilesRequest(image)
        file_name, extension = getFileNameExt(upload_name)
        reduceQualitySaveImage(upload_path, image_file, file_name, action)
        uploaded_file_url = upload_url
        printStar()
    context = {
        'form': ImageQualityForm(),
        'uploaded_file_url': uploaded_file_url,
        'action': action
    }
    return render(request, 'image-quality.html', context)



# temp
# def temp(request):
#     uploaded_file_url = None
#     action = request.GET.get('action')
#     if request.method == 'POST':
#         printStar()    
#         image = request.FILES['image']
#         action = 'pdf'
#         upload_url, upload_path, upload_name, image_file = getImagePathUrlByFilesRequest(image)
#         file_name, extension = getFileNameExt(upload_name)
#         file_name = convertAndSaveImage(upload_path, image_file, file_name, action)
#         uploaded_file_url = settings.MEDIA_URL+file_name
#         printStar()
#     context = {
#         'form': ImageToPDFForm(),
#         'uploaded_file_url': uploaded_file_url,
#         'action': action
#     }
#     return render(request, 'temp.html', context)

# def temp(request):
#     uploaded_file_url = None
#     action = request.GET.get('action')
#     if request.method == 'POST':
#         printStar()    
#         image = request.FILES['image']
#         action = 'pdf'
         
#         uploaded_file_url = settings.MEDIA_URL+file_name
#         printStar()
#     context = {
#         'form': ImageToPDFForm(),
#         'uploaded_file_url': uploaded_file_url,
#         'action': action
#     }
#     return render(request, 'temp.html', context)

def getBasePathWithFileName(file_name):
    base_path = os.path.join(settings.BASE_DIR, 'static\media'+"\\"+str(file_name))
    return base_path

# import os
# def temp(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES['image']
#         file_name = uploaded_file.name
#         printStar()
         
#         base_path = getBasePathWithFileName(file_name)
#         with open(base_path, 'wb') as f:
#             f.write(uploaded_file.read())
#             print(f.path())


#         print(base_path, "👈👈👈👈👈👈")
#         printStar()
         

#         quit()
#         # pdf_path = f'/tmp/{filename.split(".")[0]}.pdf'
#         # image = Image.open(temp_path)
#         # im = image.convert('RGB')
#         # im.save(pdf_path)

#         # fs = FileSystemStorage(pdf_path)
#         # response = FileResponse(fs.open(pdf_path, 'rb'), content_type='application/pdf')
#         # response['Content-Disposition'] = f'attachment; filename="{uuid.uuid4().hex}.pdf"'
#         # return response

#     return render(request, 'temp.html', {'form': ImageToPDFForm()})
# def temp(request):
#     if request.method=='POST':
#         printStar()
#         uploaded_file = request.FILES['image']
#         filename = uploaded_file.name


#         file_path = os.path.join(settings.STATIC_ROOT, 'hello.pdf')


#         # print(settings.MEDIA_URL)
#         # print(settings.MEDIA_ROOT)
#         temp_path = f'{filename}'
#         print("temp_path: ", temp_path)
#         with open(temp_path, 'wb') as f:
#             f.write(uploaded_file.read())

#         pdf_path = f'{filename.split(".")[0]}.pdf'

        
#         print("pdf_path: ", pdf_path)
    
#         image = Image.open(temp_path)
#         im = image.convert('RGB')
#         im.save(pdf_path)

#         print("pdf_path2: ", pdf_path)
#         fs = FileSystemStorage(pdf_path)
#         fileName = pdf_path.split("\\")[-1]
        
#         response = FileResponse(fs.open(fileName, 'rb'), content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{uuid.uuid4().hex}.pdf"'
#         printStar()
#         return response 
#     return render(request, 'temp.html', {'form':ImageToPDFForm()})


# @action(detail=False, methods=['POST'], name='Export template as pdf')
# def export(self, request, *args, **kwargs):
#     uploaded_file = request.FILES['image']
#     filename = uploaded_file.name

#     temp_path = f'/tmp/{filename}'
#     with open(temp_path, 'wb') as f:
#         f.write(uploaded_file.read())

#     pdf_path = f'/tmp/{filename.split(".")[0]}.pdf'
#     image = Image.open(temp_path)
#     im = image.convert('RGB')
#     im.save(pdf_path)

#     fs = FileSystemStorage(pdf_path)
#     response = FileResponse(fs.open(pdf_path, 'rb'), content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{uuid.uuid4().hex}.pdf"'
#     return response      
         
         

from django.shortcuts import render
from django.conf import settings
from qrcode import *
import time
from .forms import QRGenForm

# def qr_gen(request):
#     if request.method == 'POST':
#         data = request.POST['data']
#         img = make(data)
#         img_name = f'qr_{time.time()}.png'
#         img.save(settings.MEDIA_ROOT/img_name)
#         return render(request, 'qr-gen.html', {'text': text, 'img_name': img_name})
#     return render(request, 'index.html')

def qrGen(request):
    if request.method == 'POST':
        text = request.POST['text']
        img = make(text)
        img_name = f'qr_{time.time()}.png'
        img.save(settings.MEDIA_ROOT+'/'+img_name)
        uploaded_file_url = settings.MEDIA_ROOT+'/'+img_name
        return render(request, 'qr-gen.html', {'text': text, 'img_name': img_name, 'uploaded_file_url':uploaded_file_url, 'form': QRGenForm()}) 
    return render(request, 'qr-gen.html', {'form': QRGenForm()})


# Rotate Image
def imageRotate(request):
    template_name = 'image-rotate.html'
    form = ImageRotateForm()
    img_name = None  
    uploaded_file_url = None

    if request.method == 'POST':
        image = request.FILES['image']
        angle = int(request.POST.get('angle'))
        angle = angle if (angle>0 and angle<360) else 90
        # image name   
        img_name = f'imagerotate_{time.time()}.png'
        # open image
        img = Image.open(image)
        # processing
        img = img.rotate(angle)
        image.seek(0)
        # saving an image
        img.save(settings.MEDIA_ROOT+'/'+img_name)
        image.seek(0)  
        # creating url
        uploaded_file_url = settings.MEDIA_URL+'/'+img_name
    
    context =  {
        'img_name': img_name,    
        'form': form,
        'uploaded_file_url':uploaded_file_url
    }
    return render(request, template_name, context)

def imageToPDF(request):
    template_name = 'imagetopdf.html'
    form = ImageToPDFForm()
    img_name = None  
    uploaded_file_url = None

    if request.method == 'POST':
        image = request.FILES['image']
         
        # image name   
        img_name = f'imagepdf{time.time()}.pdf'
        # open image
        img = Image.open(image)
        # processing
        img = img.convert('RGB')
        img.seek(0)
        # saving an image
        img.save(settings.MEDIA_ROOT+'/'+img_name)
        img.seek(0)  
        # creating url
        uploaded_file_url = settings.MEDIA_URL+'/'+img_name
    
    context =  {
        'img_name': img_name,    
        'form': form,
        'uploaded_file_url':uploaded_file_url
    }
    return render(request, template_name, context)

def temp(request):
    template_name = 'temp.html'
    form = ImageRotateForm()
    img_name = None  
    uploaded_file_url = None

    if request.method == 'POST':
        image = request.FILES['image']
         
        # image name   
        img_name = f'imagepdf{time.time()}.pdf'
        # open image
        img = Image.open(image)
        # processing
        img = img.convert('RGB')
        img.seek(0)
        # saving an image
        img.save(settings.MEDIA_ROOT+'/'+img_name)
        img.seek(0)  
        # creating url
        uploaded_file_url = settings.MEDIA_URL+'/'+img_name
    
    context =  {
        'img_name': img_name,    
        'form': form,
        'uploaded_file_url':uploaded_file_url
    }
    return render(request, template_name, context)

