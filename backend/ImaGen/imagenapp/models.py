from django.db import models
from .utils import get_filtered_image, compressImage
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile



# Create your models here.

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


QUALITY = (
    ('NO_FILTER', 'No Filter'),
    ('PNG', 'PNG'),
    ('JPG', 'JPG'),
    ('JPED', 'JPED'),
    ('WEBP', 'WEBP'),
    ('SVG', 'SVG'),
)
class ImageQuality(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='quality')
    quality = models.CharField(max_length=100, choices=QUALITY)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     new_image = compress(self.image)
    #     self.image = new_image
    #     super().save(*args, **kwargs)

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