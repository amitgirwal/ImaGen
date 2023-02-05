from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from django.core.mail import EmailMessage

from django.http import HttpResponse


from .models import User
from .forms import *
from .tokens import account_activation_token
from imagenapp.utils import printStar

import json


# Activate link
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('home')



# User active email
def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.warning(request, f'Dear {user.name}, Please go to you email {to_email} inbox and click on received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

# def activateEmail(request, user, to_email):
#     messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
#         received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')

# User signup
def userSignup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()            
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'Successfully Signup 😊, Please check your email for confirmation.')
            return redirect('login')
        else:
            messages.error(request, form.errors)
    return render(request, 'signup.html', {'form': UserCreationForm()})


# User Login
def userLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email or Password is Wrong! 🙅")
    return render(request, 'login.html')


# Login user
@login_required
def userLogout(request):
    logout(request)
    return redirect('/')


# User account view
@login_required
def viewUser(request, pk):     
    user = get_object_or_404(User, pk=1)
    context = {
        'user': user
    }
    return render(request, 'user-profile.html', context)


# User dashboard
@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    user = request.user
    form = UserProfileForm(instance=user)
    context = {
        'form': form,
        'user': user
    }

    return render(request, template_name, context)

# loginajax
def loginajax(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        printStar()
        print(email, password)
        printStar()
        response_data = {}
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            response_data['result'] = 'failed'
            response_data['csrf_token'] = get_token(request)
            response_data['message'] = 'Email or Password is Wrong! 🙅'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Update Profile
from imagenapp.utils import printStar
def updateProfile(request):
    response_data = {}
    if request.method == 'POST':
        try:
            image = request.FILES['image'] or None
        except:
            image = None
        
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        url = request.POST.get('url')
        location = request.POST.get('location')
        
        user = User.objects.get(email=request.user.email)
        user.name = name
        if image is not None:
            user.photo = image
        user.bio = bio
        user.url = url
        user.location = location
        user.save()
        response_data['messages'] = "Profile Updated Successfully."
        response_data['image_url'] = user.photo.url
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Profile
def profile(request, username):
    template_name = 'profile.html'
    user = None
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        pass
    context = {
        'user': user
    }
    return render(request, template_name, context)


# Delete Account
def deleteAccount(request):
    if request.method == 'POST':
        user = request.user 
        user.is_active = False
        user.save()
        messages.success(request, "Your Account Deleted Successfully!")
        return redirect('home')

# Check username
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def checkUsername(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_obj = User.objects.filter(username=username).exists()
        if user_obj:
            return HttpResponse(True)
        else:
            return HttpResponse(False)

# Check Email
@csrf_exempt
def checkEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_obj = User.objects.filter(email=email).exists()
        if user_obj:
            return HttpResponse(True)
        else:
            return HttpResponse(False)


# Feedback
def feedback(request):
    template_name = 'feedback.html'
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your valuable feedback. 🤗")
            return redirect('home')
        else:
            messages.error(request, form.errors)
    context = {
        'form': form
    }
    return render(request, template_name, context)

# Subscribe
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        subs = Subscribe(email=email)
        subs.save()
        messages.success(request, "Enjoy using ImaGen and stay tuned for the latest updates and news. 🤗")
    return redirect('home')
