from django.urls import path

from . import views

urlpatterns = [
    path("slack/events", views.handle, name="handle"),
    path("slack/install", views.handle, name="install"),
    path("slack/oauth_redirect", views.handle, name="oauth_redirect"),
]
