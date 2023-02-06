from django.db import models
from .utils import get_filtered_image, compressImage
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

# Image Upload Filter
ACTION = (
    ('NO_FILTER', 'no filter'),
    ('COLORIZED', 'colorized'),
    ('GRAYSCALE', 'grayscale'),
    ('BLURRED', 'blurred'),
    ('BINARY', 'binary'),
    ('INVERT', 'invert'),
)
class Upload(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    action = models.CharField(max_length=100, choices=ACTION)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)+' | '+str(self.name)
    

    def save(self, *args, **kwargs):
        print("type in model:", type(self.image))

        # open image
        pil_img = Image.open(self.image)

        # convert the image to array and do some processing
        cv_img = np.array(pil_img)

        img = None
        if self.action in ['NO_FILTER']:
            img = get_filtered_image(cv_img, self.action)
        else:
            img = get_filtered_image(cv_img, 'NO_FILTER')
       
        # convert back to pil image
        im_pil = Image.fromarray(img)

        # save
        buffer = BytesIO()
        if self.action in ['NO_FILTER']:
            im_pil.save(buffer, format='png')
        else:
            im_pil.save(buffer, format=self.action)
        image_png = buffer.getvalue()

        self.image.save(str(self.image), ContentFile(image_png), save=False)

        super().save(*args, **kwargs)


# Image convert image
CONVERT = (
    ('NO_FILTER', 'No Filter'),
    ('PNG', 'PNG'),
    ('JPG', 'JPG'),
    ('JPED', 'JPED'),
    ('WEBP', 'WEBP'),
    ('SVG', 'SVG'),
)
class ImageConvert(models.Model):
    image = models.ImageField(upload_to='quality')
    convert = models.CharField(max_length=100, choices=CONVERT)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        pil_img = Image.open(self.image)
        cv_img = np.array(pil_img)
        img = compressImage1(cv_img, self.quality)
        im_pil = Image.fromarray(img)
        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()
        self.image.save(str(self.image), ContentFile(image_png), save=False)
        super().save(*args, **kwargs)


# Image filter  
FILTER = (
    ('NO_FILTER', 'No filter'),
    ('COLORIZED', 'Colorized'),
    ('GRAYSCALE', 'Grayscale'),
    ('BLURRED', 'Blurred'),
    ('BINARY', 'Binary'),
    ('INVERT', 'Invert'),
)
class ImageFilter(models.Model):
    image = models.ImageField(upload_to='filter')
    filter = models.CharField(max_length=100, choices=FILTER)

    def __str__(self):
        return str(self.id)


# Extract PDF
class ExtractImg(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    def __str__(self):
        return f"{self.docfile}"