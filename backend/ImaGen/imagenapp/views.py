from django.shortcuts import render, redirect, get_object_or_404
from .models import Upload
from .forms import UploadForm

from django.contrib import messages

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q



# Create your views here.
def index(request):
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            messages.success(request, "Image saved succesfully 📽️")
        else:
            messages.error(request, "Invalid Data Found 🙅")

    context = {
        'form': UploadForm(),
        'images': Upload.objects.all() 
    }
    return render(request, 'index.html', context)

def resizeImage(request):
    context = {}
    return render(request, 'index.html', context)

def imageDelete(request, pk):
    upload = get_object_or_404(Upload, id=pk)
    if upload:
        upload.delete()
        messages.success(request, "📽️ Image deleted succesfully")
    return redirect('home')

# def imageUpdate(request, pk):
#     upload = get_object_or_404(Upload, id=pk)
#     if request.method=='POST':
#         form = UploadForm(request.POST or None, instance = upload)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "📽️ Image updated succesfully")
#         else:
#             messages.error(request, "🙅 Invalid Data Found")
#     return redirect('home')


def image_view(request, pk):
    image = get_object_or_404(Upload, id=pk)
    name = image.name
    return render(request, "index.html", locals())


def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')