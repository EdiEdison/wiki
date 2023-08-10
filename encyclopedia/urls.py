from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry"),
    path("wiki/new/", views.create_entry, name="new_entry"),
    path("wiki/<str:title>/edit/", views.edit_page, name="edit"),
    path("wiki/random/page", views.random_entry_page, name="random_entry"),
]
