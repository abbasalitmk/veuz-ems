from django.urls import path
from . import views, api_views

urlpatterns = [
    # Web views
    path('', views.FormTemplateListView.as_view(), name='form_list'),
    path('create/', views.FormTemplateCreateView.as_view(), name='form_create'),
    path('<int:pk>/', views.FormTemplateDetailView.as_view(), name='form_detail'),
    path('<int:pk>/edit/', views.FormTemplateUpdateView.as_view(), name='form_edit'),
    path('<int:pk>/delete/', views.FormTemplateDeleteView.as_view(), name='form_delete'),
]

# API URL patterns
api_urlpatterns = [
    path('', api_views.FormTemplateListAPIView.as_view(), name='api_form_list'),
    path('<int:pk>/', api_views.FormTemplateDetailAPIView.as_view(), name='api_form_detail'),
    path('<int:pk>/reorder/', api_views.FormFieldReorderAPIView.as_view(), name='api_form_reorder'),
]
