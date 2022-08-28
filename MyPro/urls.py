from urllib import request
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('register/', views.register, name='register'),
    path('loginuser/', views.loginuser, name="loginuser"),
    path('logout/', views.logoutuser, name="logoutuser"),
    path('contact_form/', views.contact_form, name="contact_form"),
    path('news/<str:pk>/', views.news_detail, name='news_detail'),
]
