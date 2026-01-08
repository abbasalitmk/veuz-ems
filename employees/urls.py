from django.urls import path
from . import views, api_views

urlpatterns = [
    # Web views
    path('', views.EmployeeListView.as_view(), name='employee_list'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
]

# API URL patterns
api_urlpatterns = [
    path('', api_views.EmployeeListAPIView.as_view(), name='api_employee_list'),
    path('<int:pk>/', api_views.EmployeeDetailAPIView.as_view(), name='api_employee_detail'),
]
