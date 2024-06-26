from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  

urlpatterns = [

   path('login/', views.userLogin , name='login'),
   path('logout/', views.userLogout , name='logout'),
   path('signup/', views.userSignup , name='signup'),
   path('dashboard', views.dashboard , name='dashboard'),
   path('updateProfile', views.updateProfile, name='update_profile'),
   path('profile/<str:username>', views.profile, name='profile'),
   path('delete-account', views.deleteAccount, name='delete_account'),
   path('check-username', views.checkUsername, name='check_username'),
   path('check-email', views.checkEmail, name='check_email'),
   path('feedback', views.feedback, name='feedback'),
   path('subscribe', views.subscribe, name='subscribe'),
   
   
   
   path('view-user/<int:pk>', views.viewUser , name='view-user'),
   # path('dashboard/', views.dashboard , name='dashboard'),

   path('activate/<uidb64>/<token>', views.activate, name='activate'),

   path('view-user/<int:pk>', views.viewUser , name='view-user'),

   path('loginajax', views.loginajax , name='loginajax'),

   # Reset Password
   # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   
]