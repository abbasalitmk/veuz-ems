"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

from employees.views import DashboardView
from accounts.urls import api_urlpatterns as accounts_api_urls
from forms_builder.urls import api_urlpatterns as forms_api_urls
from employees.urls import api_urlpatterns as employees_api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Web views
    path('accounts/', include('accounts.urls')),
    path('forms/', include('forms_builder.urls')),
    path('employees/', include('employees.urls')),
    
    # API endpoints
    path('api/auth/', include(accounts_api_urls)),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/forms/', include(forms_api_urls)),
    path('api/employees/', include(employees_api_urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
