from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Employee, EmployeeFieldValue
from .serializers import EmployeeSerializer, EmployeeCreateSerializer
from forms_builder.models import FormTemplate


class EmployeeListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        employees = Employee.objects.all().prefetch_related('field_values__form_field')
        
        # Search functionality
        search = request.query_params.get('search', '')
        form_filter = request.query_params.get('form_template', '')
        
        if search:
            # Search in field values
            employee_ids = EmployeeFieldValue.objects.filter(
                value__icontains=search
            ).values_list('employee_id', flat=True)
            employees = employees.filter(id__in=employee_ids)
        
        if form_filter:
            employees = employees.filter(form_template_id=form_filter)
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_employees = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(paginated_employees, many=True)
        
        return Response({
            'success': True,
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'employees': serializer.data
        })
    
    def post(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save(created_by=request.user)
            return Response({
                'success': True,
                'message': 'Employee created successfully',
                'employee': EmployeeSerializer(employee).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response({
            'success': True,
            'employee': serializer.data
        })
    
    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeCreateSerializer(employee, data=request.data)
        if serializer.is_valid():
            employee = serializer.save(created_by=request.user)
            return Response({
                'success': True,
                'message': 'Employee updated successfully',
                'employee': EmployeeSerializer(employee).data
            })
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response({
            'success': True,
            'message': 'Employee deleted successfully'
        })
