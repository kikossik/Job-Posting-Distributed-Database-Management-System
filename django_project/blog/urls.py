from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='blog-home'),
    path('search/', views.search_results, name='search_results'),
    path('add_to_favorites/<int:job_id>/', views.add_to_favorites, name='add-to-favorites'),
    path('favorites/', views.favorite_jobs, name='favorite-jobs'),
    # path('remove-selected-favorites/', views.remove_from_favorites, name='remove-from-favorites'),
    path("about/", views.about, name='blog-about')
]
