from unicodedata import name
from django.urls import path
from .views import PostsView, PostView, categorise, category, media, edit_media


urlpatterns = [
    path('posts', PostsView.as_view(), name="posts"),
    path("post/<str:slug>", PostView.as_view(), name="post"),
    path("categories", categorise, name='categories'),
    path('category/<str:slug>', category, name="category"),
    path("medias", media, name='medias'),
    path("media/<int:id>", edit_media, name='media')
]
