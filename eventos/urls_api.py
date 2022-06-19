from django.urls import path
from eventos import views_api

urlpatterns = [
    # API
    path('get_articles/', views_api.get_articles),
    path('get_favorite_articles/', views_api.get_favorite_articles),
    path('get_article/', views_api.get_article),
    path('add_favorite_article/', views_api.add_favorite_article),
    path('remove_favorite_article/', views_api.remove_favorite_article),
    path('get_article_types/', views_api.get_article_types),
    path('read_article/', views_api.read_article),
    path('get_recommended_articles/', views_api.get_recommended_articles),
    path('send_article_comment/', views_api.send_article_comment),
    path('get_comments_article/', views_api.get_comments_article),
]