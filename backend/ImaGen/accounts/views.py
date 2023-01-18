from django.shortcuts import render, redirect, get_object_or_404

from .models import User
from .forms import UserCreationForm, UserEditForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# User signup
def userSignup(request):
    msg = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'msg':'Successfully Signup 😊', 'status':'success'})
        else:
            msg = form.errors
    form = UserCreationForm()
    context = {
        'form':form,
        'msg':msg
    }
    return render(request, 'signup.html', context)

# User Login
def userLogin(request):
    msg = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        print("user", user, email, password)
        print("dfjjsdfjsjdfhkjshdfkjhsdkjhfkjshdfkjhsdjhf")
        if user is not None:
            login(request, user)
            print("login sdfjdsfjldsjfkljhjsdjfhkljsdfkl##########")
            return redirect('home')
        else:
            msg = "Email or Password is Wrong!!!"
    context = {
        'msg': msg
    }
    return render(request, 'login.html', context)


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
