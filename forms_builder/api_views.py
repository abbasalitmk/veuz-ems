from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import FormTemplate, FormField
from .serializers import FormTemplateSerializer, FormTemplateCreateSerializer, FormFieldSerializer


class FormTemplateListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        form_templates = FormTemplate.objects.all()
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_templates = paginator.paginate_queryset(form_templates, request)
        serializer = FormTemplateSerializer(paginated_templates, many=True)
        
        return Response({
            'success': True,
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'form_templates': serializer.data
        })
    
    def post(self, request):
        serializer = FormTemplateCreateSerializer(data=request.data)
        if serializer.is_valid():
            form_template = serializer.save(created_by=request.user)
            return Response({
                'success': True,
                'message': 'Form template created successfully',
                'form_template': FormTemplateSerializer(form_template).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class FormTemplateDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        form_template = get_object_or_404(FormTemplate, pk=pk)
        serializer = FormTemplateSerializer(form_template)
        return Response({
            'success': True,
            'form_template': serializer.data
        })
    
    def put(self, request, pk):
        form_template = get_object_or_404(FormTemplate, pk=pk)
        serializer = FormTemplateCreateSerializer(form_template, data=request.data)
        if serializer.is_valid():
            form_template = serializer.save()
            return Response({
                'success': True,
                'message': 'Form template updated successfully',
                'form_template': FormTemplateSerializer(form_template).data
            })
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        form_template = get_object_or_404(FormTemplate, pk=pk)
        form_template.delete()
        return Response({
            'success': True,
            'message': 'Form template deleted successfully'
        })


class FormFieldReorderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        form_template = get_object_or_404(FormTemplate, pk=pk)
        field_order = request.data.get('field_order', [])
        
        with transaction.atomic():
            for index, field_id in enumerate(field_order):
                FormField.objects.filter(id=field_id, form_template=form_template).update(order=index)
        
        return Response({
            'success': True,
            'message': 'Fields reordered successfully'
        })
