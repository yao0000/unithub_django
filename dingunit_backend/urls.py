"""
URL configuration for dingunit_backend project.

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

from controller import UserController, DraftController, ReservationController, SessionController

urlpatterns = [
    path('dingunit_backend/login/', UserController.login),
    path('dingunit_backend/register/', UserController.register),
    path('dingunit_backend/users/', UserController.get_users_list),
    path('dingunit_backend/update_accRight/', UserController.update_access_right),
    path('dingunit_backend/get_user_details/', UserController.get_user_details),
    path('dingunit_backend/delete_user/', UserController.delete_user),

    path('dingunit_backend/get_draft_list/', DraftController.get_draft_list),
    path('dingunit_backend/get_draft_details/', DraftController.get_draft_details),
    path('dingunit_backend/post_draft_data/', DraftController.post_draft_data),
    path('dingunit_backend/update_draft_details/', DraftController.update_draft_details),
    path('dingunit_backend/delete_draft_data/', DraftController.delete_draft_data),
    
    path('dingunit_backend/get_reservation_list/', ReservationController.get_reservation_list),
    path('dingunit_backend/post_reservation/', ReservationController.post_reservation),

    path('dingunit_backend/run_reserve/', SessionController.run_reserve),
    
]
