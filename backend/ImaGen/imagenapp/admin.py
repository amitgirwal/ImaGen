from django.contrib import admin
from .models import Upload, ImageConvert, ImageFilter

# Register your models here.
admin.site.register(Upload)
admin.site.register(ImageConvert)
admin.site.register(ImageFilter)