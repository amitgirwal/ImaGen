import cv2
from django.core.files.storage import FileSystemStorage

import os
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest, HttpResponseNotAllowed
 
from django.utils.decorators import method_decorator
from django.http import Http404
from django.conf import settings

from PIL import Image, ImageFilter, ImageEnhance, ImageOps


def compressImage(image, action):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
     
    if action == 'NO_FILTER':
        filtered = image
    return filtered

def get_filtered_image(image, action):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    filtered = None

    # if action == 'PNG':
    #     filtered = image
    #     cv2.imwrite(filename, img)
    #     return filtered
    if action == 'NO_FILTER':
        filtered = image
    elif action == 'COLORIZED':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif action == 'GRAYSCALE':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif action == 'BLURRED':
        width, height = img.shape[:2]
        if width > 500:
            k = (50, 50)
        elif width > 200 and width <=500:
            k = (25,25)
        else:
            k = (10,10)
        blur = cv2.blur(img, k)
        filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    elif action == 'BINARY':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    elif action == 'INVERT':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        filtered = cv2.bitwise_not(img)
    return filtered


def get_file_size_in_bytes(file_path):
   """ Get size of file at given path in bytes"""
   size = os.path.getsize(file_path)
   return size

def convert_to_webp(filename, path="images/"):
    extension = filename.split('.')[-1]
    fname = filename.split('.')[0]
    img = Image.open(path + filename)

    if extension == "png":
        img.save((path+fname+".webp"), "webp", lossless=True)
    elif extension == "jpg" or extension == "jpeg":
        img.save((path+fname+".webp"), "webp", quality=85)

def convert_all(path="images/"):
    for root, dirs, files in os.walk(path):
        for imagefile in files:
            if imagefile.endswith(".png") or imagefile.endswith(".jpg") or imagefile.endswith(".jpeg"):
                convert_to_webp(imagefile, os.path.join(root, ""))


# Image Convert Path: static/media
def printStar():
	print('\n\n')
	print('#'*100)

def getFileNameExt(upload_name):
    file_name = upload_name.split('.')[0]
    extension = upload_name.split('.')[-1]
    return file_name, extension

def getImagePathUrlByFilesRequest(req_image):
    fs = FileSystemStorage()
    image_file = fs.save(str(req_image), ContentFile(req_image.read()))
    upload_url = fs.url(image_file)
    upload_path = fs.path(image_file)
    upload_name = str(image_file)
    return upload_url, upload_path, upload_name, image_file

def convertAndSaveImage(upload_path, image_file, file_name, action):
    action = action.lower()
    img = Image.open(upload_path)
    file_name, extension = getFileNameExt(upload_path)
    file_url_name = file_name.split("\\")[-1] +'.'+action

    if action == extension:
        return 
    if action == 'png':
        img.save(file_name+'.png', "png", lossless=True)
    elif action == 'jpg':
        img.save(file_name+'.jpg', "jpg", lossless=True)
    elif action == 'jpeg':
        img.save(file_name+'.jpeg', "jpeg", lossless=True)
    elif action == 'webp':
        img.save(file_name+'.webp', "webp", quality=85)
    elif action == 'svg':
        img.save(file_name+'.svg', "svg", quality=65)
    else:
        return 
    return file_url_name

  
def reduceQualitySaveImage(upload_path, image_file, file_name, action):
    action = int(action)
    img = Image.open(upload_path)
    file_name, extension = getFileNameExt(upload_path)
    file_url_name = upload_path
    if type(action) is int and (action>1 and action<100):
        action = action
    else:
        action = 95
    print('file_url_name: ', file_url_name,  type(action))
    print('quality: ', action)
    img.save(file_url_name, quality=action)
    return file_url_name


# ACTION = (
#     ('NO_FILTER', 'no filter'),
#     ('COLORIZED', 'colorized'),
#     ('GRAYSCALE', 'grayscale'),
#     ('BLURRED', 'blurred'),
#     ('BINARY', 'binary'),
#     ('INVERT', 'invert'),
# )
def filterSaveImage(upload_path, image_file, file_name, action):
    img = Image.open(upload_path)
    file_name, extension = getFileNameExt(upload_path)
    file_url_name = file_name.split("\\")[-1] +'.'+action

    if action == 'NO_FILTER':
        img.save(upload_path, "png", lossless=True)
    elif action == 'COLORIZED':
        img = ImageOps.colorize(img, black ="blue", white ="white")
        img.save(upload_path, "png", lossless=True)
    elif action == 'GRAYSCALE':
        img = ImageOps.grayscale(img)
        img.save(upload_path, "png", lossless=True)
    elif action == 'BLURRED':
        img = img.filter(ImageFilter.BLUR)
        img.save(upload_path, "png", lossless=True)
    elif action == 'BINARY':
        img.save(upload_path, "png", lossless=True)
    elif action == 'INVERT':
        img.save(upload_path, "png", lossless=True)
    return file_url_name

# image, action
# def filterSaveImage(upload_path, image_file, file_name, action):
#     pil_img = Image.open(image_file)
#     image = image_file
#     cv_img = np.array(pil_img)
#     img = None
#     img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     filtered = None
#     if action == 'NO_FILTER':
#         filtered = image
#     elif action == 'COLORIZED':
#         filtered = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     elif action == 'GRAYSCALE':
#         filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     elif action == 'BLURRED':
#         width, height = img.shape[:2]
#         if width > 500:
#             k = (50, 50)
#         elif width > 200 and width <=500:
#             k = (25,25)
#         else:
#             k = (10,10)
#         blur = cv2.blur(img, k)
#         filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
#     elif action == 'BINARY':
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
#     elif action == 'INVERT':
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
#         filtered = cv2.bitwise_not(img)
    
#     img = filtered
#     im_pil = Image.fromarray(img)
#     buffer = BytesIO() 
#     im_pil.save(buffer, format='png')
#     image_png = buffer.getvalue()

#     return image_png



import img2pdf 

def imgToPDF(upload_path, image_file, file_name):
    file_name, extension = getFileNameExt(upload_path)
    file_url_name = file_name.split("\\")[-1] +'.pdf'

    img = Image.open(upload_path)
    img = img.convert('RGB')  
    img.save(file_url_name, format="PDF")
    print(file_url_name)
    print(file_name)
    print(extension)
    return file_url_name
    # img = Image.open(upload_path)
    # file_name, extension = getFileNameExt(upload_path)
    # file_url_name = file_name.split("\\")[-1] +'.pdf'

    # # converting into chunks using img2pdf 
    # pdf_bytes = img2pdf.convert(image_file) 
    
    # # img.save(upload_path, "png", lossless=True)
    # # opening or creating pdf file 
    # file = open(pdf_path, "wb") 

    # # writing pdf files with chunks 
    # file.write(pdf_bytes) 

    # # closing image file 
    # img.close() 

    # # closing pdf file 
    # file.close() 
    # return file_url_name





# add text to an image
# import cv2

# image = 'blagaj_original.jpg'
# img =  cv2.imread(image)

# height, width, depth = img.shape
# desired_height = 512
# aspect_ratio = desired_height/width
# dimension = (desired_height, int(height*aspect_ratio) )
# img_resized = cv2.resize(img, dimension)

# BLACK = (255,255,255)
# font = cv2.FONT_HERSHEY_SIMPLEX
# font_size = 1.1
# font_color = BLACK
# font_thickness = 2
# text = 'amehta.github.io'
# x,y = 10,650
# img_text = cv2.putText(img_resized, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

# cv2.imshow("Resized", img_text)
# cv2.waitKey(0)

# cv2.imwrite('blagaj_resized_text.jpg', img_text)