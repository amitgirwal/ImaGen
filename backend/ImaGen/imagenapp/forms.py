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



class ImageToPDFForm(forms.Form):
    image = forms.ImageField()


class QRGenForm(forms.Form):
    text = forms.CharField(max_length=500, initial="Hola, 🤗")


class ImageRotateForm(forms.Form):
    image = forms.ImageField()
    angle = forms.CharField(max_length=500, initial="90")


FILTER_COLOR = (
    ('sepia', 'Sepia'),
    ('red', 'Red'),
    ('skyblue', 'Sky Blue'),
    ('darkpink', 'Dark Pink'),
    ('lemonyellow', 'Lemon Yellow'),
    ('darkgrey', 'Dark Grey'),
)

class ColorizedFilterForm(forms.Form):
    image = forms.ImageField()
    filter_color = forms.ChoiceField(
        required=True,
        choices=FILTER_COLOR
    )