from django.shortcuts import render, redirect
from .models import Upload
from .forms import UploadForm

from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    msg = ''
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            msg = 'Image saved succesfully!!!'
        else:
            msg = form.errors
            print(form.errors)
    context = {
        'form': UploadForm(),
        'images': Upload.objects.all(),
        'msg': msg
    }
    return render(request, 'index.html', context)

def resizeImage(request):
    context = {}
    return render(request, 'index.html', context)




def temp(request):
    return render(request, 'imagenapp/temp.html')

