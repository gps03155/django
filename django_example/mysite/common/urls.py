# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = "common"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="common/login.html"), name="login"),
]
