from django.urls import path
from usuarios import views_api

urlpatterns = [
    # API
    path('login/', views_api.login),
    path('register/', views_api.register),
    path('logout/', views_api.logout),
]