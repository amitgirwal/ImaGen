from django import forms
from .models import Upload, ImageConvert, ImageFilter


# Img Gen Form
class ImgGenForm(forms.Form):
    text = forms.CharField(max_length=500, initial="a raccoon astronaut with the cosmos reflecting on the glass of his helmet dreaming of the stars")

# QR Gen Form
class QRGenForm(forms.Form):
    text = forms.CharField(max_length=500, initial="Hola, 🤗")


# Image 2 PDF Form
class ImageToPDFForm(forms.Form):
    image = forms.ImageField()


# Colorize Image Filter Form
FILTER_COLOR = (
    ('sepia', 'Sepia'),
    ('red', 'Red'),
    ('skyblue', 'Sky Blue'),
    ('darkpink', 'Dark Pink'),
    ('lemonyellow', 'Lemon Yellow'),
    ('darkgrey', 'Dark Grey'),
)

class ColorizeFilterForm(forms.Form):
    image = forms.ImageField()
    filter_color = forms.ChoiceField(
        required=True,
        choices=FILTER_COLOR
    )


# Image Convert Form
CONVERT = (
    ('WEBP', 'WEBP'),
    ('PNG', 'PNG'),
    ('JPG', 'JPG'),
    ('JPEG', 'JPEG')
)

class ImageConvertForm(forms.Form):
    image = forms.ImageField()
    convert = forms.ChoiceField(
        required=True,
        choices=CONVERT
    )


# Reduce Image Quality Form
class ImageQualityForm(forms.Form):
    image = forms.ImageField()
    quality = forms.CharField(max_length=200, initial=95)


# Rotate Image Form
class ImageRotateForm(forms.Form):
    image = forms.ImageField()
    angle = forms.CharField(max_length=10, initial="90")
    expand = forms.BooleanField(required=False, initial=False)


# Flip Image Form
FLIP_OPTIONS = (
    ('FLIP_TOP_BOTTOM', 'Flip Top To Bottom'),
    ('FLIP_LEFT_RIGHT', 'Flip Left To Right'),
    ('ROTATE_90', 'Rotate 90 degree'),
    ('ROTATE_180', 'Rotate 180 degree'),
    ('ROTATE_270', 'Rotate 270 degree'),
    ('TRANSVERSE', 'Transverse'),
)

class ImageFlipForm(forms.Form):
    image = forms.ImageField()
    flip_options = forms.ChoiceField(
        required=True,
        choices=FLIP_OPTIONS
    )


########################################
class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'

# class ImageConvertForm(forms.ModelForm):
#     class Meta:
#         model = ImageConvert
#         fields =  '__all__'

class ImageFilterForm(forms.ModelForm):
    class Meta:
        model = ImageFilter
        fields =  '__all__'


# Extract Img From
class ExtractImgFrom(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )