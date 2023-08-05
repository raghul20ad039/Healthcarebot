from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("livechat", views.livechat, name="livechat"),
    path("login", views.login, name="login"),
    path("logout",views.logout,name="logout"),
    path("register", views.register, name="register"),
    path("services", views.services, name="services"),
    path("dashboard", views.dashboard, name="dashboard"),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]
