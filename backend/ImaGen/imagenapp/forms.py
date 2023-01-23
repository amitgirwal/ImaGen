from django import forms
from .models import Upload, ImageConvert, ImageFilter

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'

class ImageConvertForm(forms.ModelForm):
    class Meta:
        model = ImageConvert
        fields =  '__all__'

class ImageFilterForm(forms.ModelForm):
    class Meta:
        model = ImageFilter
        fields =  '__all__'

class ImageQualityForm(forms.Form):
    image = forms.ImageField()
    quality = forms.CharField(max_length=200, initial=95)

    