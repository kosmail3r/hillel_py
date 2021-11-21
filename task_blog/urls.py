from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post-edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('post-delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('create_post/', views.PostCreate.as_view(), name='post_create'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
]
