from django import forms
from .models import Upload

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'