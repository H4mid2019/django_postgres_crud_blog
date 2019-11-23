from django.urls import path
from .views import PostsView, PostView


urlpatterns = [
    path('posts', PostsView.as_view(), name="posts"),
    path("post/<str:slug>", PostView.as_view(), name="post")
]