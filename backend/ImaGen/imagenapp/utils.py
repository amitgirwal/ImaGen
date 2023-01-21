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

from PIL import Image, ImageFilter, ImageEnhance

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


from PIL import Image
import os

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


