from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView

from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('/posts', PostListView.as_view(), name='posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('create', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]