from django.urls import path

from . import views

urlpatterns = [
    path("slack/events", views.events, name="handle"),
    path("slack/install", views.oauth, name="install"),
    path("slack/oauth_redirect", views.oauth, name="oauth_redirect"),
]
