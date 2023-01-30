from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib import messages

# custom import
from .models import Upload, ImageConvert, ImageFilter
from .forms import UploadForm, ImageConvertForm, ImageFilterForm, ImageQualityForm, ImageToPDFForm, ImageRotateForm, QRGenForm, ColorizedFilterForm

# image utils
from .utils import getImagePathUrlByFilesRequest, convertAndSaveImage, getFileNameExt, printStar, reduceQualitySaveImage, filterSaveImage, imgToPDF

# storage
from django.core.files.storage import FileSystemStorage

# settings
from django.conf import settings

# images
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

# qr code
from qrcode import *
 
# default modules
import time
import json



# Functions 
# use this template for function creation 👈👈👈👈👈
# def functName(request):
#     template_name = 'template_name.html'
#     form = ImageForm()
#     img_name = None  
#     uploaded_file_url = None

#     if request.method == 'POST':
#         image = request.FILES['image']
         
#         # image name   
#         img_name = f'image-filter{time.time()}.png'
#         # open image
#         img = Image.open(image)
#         img = img.convert('RGB')

#         # processing => Write image processing code here
#         img.seek(0)
#         # saving an image
#         img.save(settings.MEDIA_ROOT+'/'+img_name)
#         img.seek(0)  
#         # creating url
#         uploaded_file_url = settings.MEDIA_URL+'/'+img_name
    
#     context =  {
#         'img_name': img_name,    
#         'form': form,
#         'uploaded_file_url':uploaded_file_url
#     }
#     return render(request, template_name, context)


# home page
def index(request):
    return render(request, 'index.html')

# qr code 
def qrGen(request):
    template_name = 'qr-gen.html'
    form = QRGenForm()
    img_name = None  
    uploaded_file_url = None
    text = None

    if request.method == 'POST':
        text = request.POST.get('text')
        img = make(text)
        img_name = f'qr_{time.time()}.png'
        img.save(settings.MEDIA_ROOT+'/'+img_name)
        uploaded_file_url = settings.MEDIA_ROOT+'/'+img_name

    context =  {
        'text': text, 
        'img_name': img_name,    
        'form': form,
        'uploaded_file_url':uploaded_file_url
    }
    return render(request, template_name, context)


# Image To PDF
def imageToPDF(request):
    template_name = 'image-to-pdf.html'
    form = ImageToPDFForm()
    img_name = None  
    uploaded_file_url = None

    if request.method == 'POST':
        image = request.FILES['image']
        img_name = f'imagepdf{time.time()}.pdf'
        
        img = Image.open(image)
        img = img.convert('RGB')
        img.seek(0)
        img.save(settings.MEDIA_ROOT+'/'+img_name)
        img.seek(0)  
        
        uploaded_file_url = settings.MEDIA_URL+'/'+img_name
    
    context =  {
        'img_name': img_name,    
        'form': form,
        'uploaded_file_url':uploaded_file_url
    }
    return render(request, template_name, context)




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
         
         



# def qr_gen(request):
#     if request.method == 'POST':
#         data = request.POST['data']
#         img = make(data)
#         img_name = f'qr_{time.time()}.png'
#         img.save(settings.MEDIA_ROOT/img_name)
#         return render(request, 'qr-gen.html', {'text': text, 'img_name': img_name})
#     return render(request, 'index.html')



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



# def temp(request):
#     template_name = 'temp.html'
#     form = ImageRotateForm()
#     img_name = None  
#     uploaded_file_url = None

#     if request.method == 'POST':
#         image = request.FILES['image']
         
#         # image name   
#         img_name = f'imagepdf{time.time()}.pdf'
#         # open image
#         img = Image.open(image)
#         # processing
#         img = img.convert('RGB')
#         img.seek(0)
#         # saving an image
#         img.save(settings.MEDIA_ROOT+'/'+img_name)
#         img.seek(0)  
#         # creating url
#         uploaded_file_url = settings.MEDIA_URL+'/'+img_name
    
#     context =  {
#         'img_name': img_name,    
#         'form': form,
#         'uploaded_file_url':uploaded_file_url
#     }
#     return render(request, template_name, context)



def red(r,g,b):
    newr = r
    newg = 0
    newb = 0
    return (newr,newg,newb)

def darkpink(r,g,b):
    newr = g
    newg = b
    newb = r
    return (newr,newg,newb)
def skyblue(r,g,b):
    newr = b
    newg = g
    newb = r
    return (newr,newg,newb)
def lemonyellow(r,g,b):
    newr = g
    newg = r
    newb = b
    return (newr,newg,newb)
def grey(r,g,b):
    newr = (r+g+b)//3
    newg = (r+g+b)//3
    newb = (r+g+b)//3
    return (newr,newg,newb)
def sepia(r,g,b):
    newr = int((r * .393) + (g *.769) + (b * .189))
    newg = int((r * .349) + (g *.686) + (b * .168))
    newb = int((r * .272) + (g *.534) + (b * .131))
    return (newr,newg,newb)

def tempa(request):
    template_name = 'temp.html'
    form = ImageRotateForm()
    img_name = None  
    uploaded_file_url = None

    if request.method == 'POST':
        image = request.FILES['image']
         
        # image name   
        img_name = f'imagefilter{time.time()}.png'
        # open image
        img = Image.open(image).convert('RGB')
        # processing
        # gather width, height
        width, height = img.size
        # load pixels
        pixels = img.load()
        # choice
        no = int(3)
        for py in range(height):
            for px in range(width):
                r, g, b = img.getpixel((px,py))
                if no == 1:
                    pixels[px,py] = red(r,g,b)
                elif no == 2:
                    pixels[px,py] = darkpink(r,g,b)
                elif no == 3:
                    pixels[px,py] = skyblue(r,g,b)
                elif no == 4:
                    pixels[px,py] = lemonyellow(r,g,b)
                elif no == 5:
                    pixels[px,py] = grey(r,g,b)
                elif no == 6:
                    pixels[px,py] = sepia(r,g,b)
                else:
                    pixels[px,py] = (r,g,b) 
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



def hex_to_rgb(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)
  
  return tuple(rgb)

def addColor(r,g,b):
    newr = r
    newg = g
    newb = b
    return (newr,newg,newb) 


def tempAjax(request):
    if request.method == 'POST':
        image = request.FILES['image']
        print("##########################=>>>>>>>>>>>>>>>>: ", image)
        color = request.POST.get('color')
        newr, newg, newb = hex_to_rgb(color[1:])
        print(newr, newg, newb)
        # image name   
        img_name = f'imagefilter{time.time()}.png'
        # open image
        img = Image.open(image)
        img = img.convert('RGB')
        # processing
        # gather width, height
        width, height = img.size
        # load pixels
        pixels = img.load()
        # choice
        for py in range(height):
            for px in range(width):
                r, g, b = img.getpixel((px,py))
                pixels[px,py] = grey(r, g, b)
        
        # saving an image
        img.save(settings.MEDIA_ROOT+'/'+img_name)
        # creating url
        uploaded_file_url = settings.MEDIA_URL+'/'+img_name
        response_data = {}
        response_data['error'] = 'success=>'+str(color)
        response_data['uploaded_file_url'] = str(uploaded_file_url)
        response_data['message'] = 'Email or Password is Wrong! 🙅'
        printStar()
        print(response_data)
        print(r,g,b)
        printStar()
    return HttpResponse(json.dumps(response_data), content_type="application/json")




# Template use this 👈👈👈👈👈
# def colorizedFilter(request):
#     template_name = 'color-filter.html'
#     form = ColorizedFilterForm()
#     img_name = None  
#     uploaded_file_url = None

#     if request.method == 'POST':
#         image = request.FILES['image']
         
#         # image name   
#         img_name = f'image-filter{time.time()}.png'
#         # open image
#         img = Image.open(image)
#         img = img.convert('RGB')

#         # processing => Write image processing code here
        



#         img.seek(0)
#         # saving an image
#         img.save(settings.MEDIA_ROOT+'/'+img_name)
#         img.seek(0)  
#         # creating url
#         uploaded_file_url = settings.MEDIA_URL+'/'+img_name
    
#     context =  {
#         'img_name': img_name,    
#         'form': form,
#         'uploaded_file_url':uploaded_file_url
#     }
#     return render(request, template_name, context)

# Red filter
def red(r,g,b):
    newr = r
    newg = 0
    newb = 0
    return (newr,newg,newb)

# Dark Pink Filter
def darkpink(r,g,b):
    newr = g
    newg = b
    newb = r
    return (newr,newg,newb)

# Sky Blue Filter => red color
def skyblue(r,g,b):
    newr = b
    newg = g
    newb = r
    return (newr,newg,newb)

# lemon green
def lemonyellow(r,g,b):
    newr = g
    newg = r
    newb = b
    return (newr,newg,newb)

# darkgrey
def darkgrey(r,g,b):
    newr = (r+g+b)//3
    newg = (r+g+b)//3
    newb = (r+g+b)//3
    return (newr,newg,newb)

def sepia(r,g,b):
    newr = int((r * .393) + (g *.769) + (b * .189))
    newg = int((r * .349) + (g *.686) + (b * .168))
    newb = int((r * .272) + (g *.534) + (b * .131))
    return (newr,newg,newb)

def colorizedFilter(request):
    template_name = 'color-filter.html'
    form = ColorizedFilterForm()
    img_name = None  
    uploaded_file_url = None

    if request.method == 'POST':
        image = request.FILES['image']
        check = request.POST.get('filter_color')
        printStar() 

        # image name   
        img_name = f'image-filter{time.time()}.png'
         
         
        # open image
        img = Image.open(image)
        img = img.convert('RGB')

        # processing => Write image processing code here
        width, height = img.size
        pixels = img.load()
        for py in range(height):
            for px in range(width):
                r, g, b = img.getpixel((px,py))
                if check == 'sepia':
                    pixels[px,py] = sepia(r,g,b)
                elif check == 'red':
                    pixels[px,py] = red(r,g,b)        
                elif check == 'skyblue':
                    pixels[px,py] = skyblue(r,g,b)
                elif check == 'darkpink':
                    pixels[px,py] = darkpink(r,g,b)        
                elif check == 'lemonyellow':
                    pixels[px,py] = lemonyellow(r,g,b)
                elif check == 'darkgrey':
                    pixels[px,py] = darkgrey(r,g,b)

        # saving an image
        img.seek(0)
        img.save(settings.MEDIA_ROOT+'/'+img_name)
        img.seek(0)

        # creating url
        uploaded_file_url = settings.MEDIA_URL+'/'+img_name

        print('uploaded_file_url: ', uploaded_file_url)

        printStar()
    context =  {
        'img_name': img_name,    
        'form': form,
        'uploaded_file_url':uploaded_file_url
    }
    return render(request, template_name, context)