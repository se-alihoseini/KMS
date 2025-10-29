from django.urls import path

from account.api.v1 import views

account_url_patterns = [
    path("register/", views.user_register, name="user_register"),
    path("test-user/", views.test_user, name="test-user"),
    path("login/", views.user_login, name="user-login"),
]