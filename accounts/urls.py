from django.urls import path
from . import views, api_views

urlpatterns = [
    # Web views
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]

# API URL patterns
api_urlpatterns = [
    path('login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('profile/', api_views.ProfileAPIView.as_view(), name='api_profile'),
    path('change-password/', api_views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('logout/', api_views.LogoutAPIView.as_view(), name='api_logout'),
]
