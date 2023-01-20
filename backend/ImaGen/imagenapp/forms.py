from django import forms
from .models import Upload, ImageQuality

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'


 
class ImageConvertForm(forms.ModelForm):
     
    class Meta:
        model = ImageQuality
        fields =  '__all__'