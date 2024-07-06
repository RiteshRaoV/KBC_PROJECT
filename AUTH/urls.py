# accounts/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/',views.home,name='home'),
    path('password-reset/', views.password_reset_link, name='password_reset'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_link_check, name='reset_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
