from django.urls import path

from account.api.v1 import views

account_url_patterns = [
    path("test-user/", views.test_user, name="test-user"),
]