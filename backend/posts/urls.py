from django.urls import path
from .views import post_content, save_draft, schedule_post, list_posts

urlpatterns = [
    path('post/', post_content),
    path('list-posts/', list_posts),
    path('save-draft/', save_draft),
    path('schedule-post/', schedule_post),
]
