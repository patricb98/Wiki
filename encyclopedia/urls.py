from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>",views.title, name = "title"),
    path("create/", views.new_page, name="new_page"),
    path("<str:title>/edit/", views.edit_page, name="edit_page"),
    path("random/", views.random_page, name="random_page")
]
