from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), # url path for homepage
    path("wiki/<str:title>", views.generate_page, name="page"), # url path for each wiki page
    path("search", views.search_page, name="search"), # url path for when users submit search bar
    path("newpage", views.new_page, name="new"), # url path for when users upload new page
    path("edit/<str:title>", views.edit_page, name="edit"), # url path for users to edit current page
    path("random", views.random_page, name="random"), # url path for a random wiki page
]
