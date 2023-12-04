from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("new_author/", views.new_author, name="new_author"),
    path("new_tag/", views.new_tag, name="new_tag"),
    path("new_quote/", views.new_quote, name="new_quote"),
    path("author/<str:author_fn>", views.author, name="author"),
    path("tag/<str:tag_name>", views.tag, name="tag"),
]
