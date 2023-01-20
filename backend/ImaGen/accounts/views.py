from django.shortcuts import render, redirect, get_object_or_404

from .models import User
from .forms import UserCreationForm, UserEditForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token


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



def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': 'helloworld',
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
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
            user = form.save(commit=False)
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


# User Login
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



def dashboard(request):
    post_count = Post.objects.filter(auther=request.user).count() 
    posts = Post.objects.filter(auther=request.user)
    post_likes = 0
    for post in posts:
       post_likes += post.likes.count() 

    msg = ''
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user )
        if form.is_valid():
            form.save()
            msg = 'Successfully profile updated!!'
        else:
            msg = form.errors
            
    form = UserEditForm(instance=user)
    followers = 0
    following = 0 
    context = {
        'user':request.user,
        'post_count':post_count,
        'post_likes':post_likes,
        'followers': followers,
        'following': following,
        'msg': msg,
        'form': form
    }
    return render(request, 'dashboard.html', context)