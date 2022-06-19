from django.urls import path
from usuarios import views_api

urlpatterns = [
    # API
    path('login/', views_api.login),
    path('register/', views_api.register),
    path('logout/', views_api.logout),
    path('change_credentials/', views_api.change_credentials),
    path('chage_profile_picture/', views_api.change_profile_picture),
    path('remove_profile_picture/', views_api.remove_profile_picture),
]