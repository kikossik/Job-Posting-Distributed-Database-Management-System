from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path("", views.home, name='blog-home'),
    path("user/<str:username>", UserPostListView.as_view(), name='user-posts'),
    path("job/<int:pk>/", PostDetailView.as_view(), name='job-detail'),
    path("job/new/", PostCreateView.as_view(), name='job-create'),
    path("job/<int:pk>/update/", PostUpdateView.as_view(), name='job-update'),
    path("job/<int:pk>/delete/", PostDeleteView.as_view(), name='job-delete'),
    path("about/", views.about, name='blog-about'),
    path('search/', views.search_results, name='search_results'),
]