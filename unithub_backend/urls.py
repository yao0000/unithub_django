"""
URL configuration for unithub_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from controller import UserController, ClientDataController

urlpatterns = [
    path('unithub_backend/login/', UserController.login),
    path('unithub_backend/register/', UserController.register),
    path('unithub_backend/users/', UserController.get_users_list),
    path('unithub_backend/update_accRight/', UserController.update_access_right),
    path('unithub_backend/get_user_details/', UserController.get_user_details),
    path('unithub_backend/get_client_data_list/', ClientDataController.get_client_data_list),
    path('unithub_backend/post_client_data/', ClientDataController.post_client_data),
]
