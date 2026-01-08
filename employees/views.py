from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.db import transaction
import json

from .models import Employee, EmployeeFieldValue
from forms_builder.models import FormTemplate, FormField


class DashboardView(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request, 'dashboard.html')


class EmployeeListView(LoginRequiredMixin, View):
    
    def get(self, request):
        employees = Employee.objects.all().prefetch_related('field_values__form_field')
        form_templates = FormTemplate.objects.all()
        
        # Search functionality
        search = request.GET.get('search', '')
        form_filter = request.GET.get('form_template', '')
        
        if search:
            # Search in field values
            employee_ids = EmployeeFieldValue.objects.filter(
                value__icontains=search
            ).values_list('employee_id', flat=True)
            employees = employees.filter(id__in=employee_ids)
        
        if form_filter:
            employees = employees.filter(form_template_id=form_filter)
        
        # Prepare employee data with field values
        employee_list = []
        for emp in employees:
            emp_data = {
                'id': emp.id,
                'form_template': emp.form_template.name,
                'created_at': emp.created_at,
                'fields': {fv.form_field.label: fv.value for fv in emp.field_values.all()}
            }
            employee_list.append(emp_data)
        
        return render(request, 'employees/employee_list.html', {
            'employees': employee_list,
            'form_templates': form_templates,
            'search': search,
            'form_filter': form_filter
        })


class EmployeeCreateView(LoginRequiredMixin, View):
    
    def get(self, request):
        form_templates = FormTemplate.objects.all()
        selected_template_id = request.GET.get('template')
        selected_template = None
        
        if selected_template_id:
            selected_template = get_object_or_404(FormTemplate, pk=selected_template_id)
        
        return render(request, 'employees/employee_create.html', {
            'form_templates': form_templates,
            'selected_template': selected_template
        })
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            form_template_id = data.get('form_template')
            field_values = data.get('field_values', {})
            
            if not form_template_id:
                return JsonResponse({'success': False, 'message': 'Form template is required'}, status=400)
            
            form_template = get_object_or_404(FormTemplate, pk=form_template_id)
            
            # Validate required fields
            for field in form_template.fields.filter(required=True):
                if str(field.id) not in field_values or not field_values[str(field.id)]:
                    return JsonResponse({
                        'success': False, 
                        'message': f'{field.label} is required'
                    }, status=400)
            
            with transaction.atomic():
                # Create employee
                employee = Employee.objects.create(
                    form_template=form_template,
                    created_by=request.user
                )
                
                # Create field values
                for field_id, value in field_values.items():
                    try:
                        form_field = FormField.objects.get(id=int(field_id))
                        EmployeeFieldValue.objects.create(
                            employee=employee,
                            form_field=form_field,
                            value=value
                        )
                    except FormField.DoesNotExist:
                        pass
            
            return JsonResponse({
                'success': True,
                'message': 'Employee created successfully',
                'id': employee.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class EmployeeDetailView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        field_values = employee.field_values.all().select_related('form_field')
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'id': employee.id,
                'form_template': employee.form_template.id,
                'form_template_name': employee.form_template.name,
                'field_values': [
                    {
                        'field_id': fv.form_field.id,
                        'label': fv.form_field.label,
                        'value': fv.value,
                        'field_type': fv.form_field.field_type
                    }
                    for fv in field_values
                ],
                'created_at': employee.created_at.isoformat()
            })
        
        return render(request, 'employees/employee_detail.html', {
            'employee': employee,
            'field_values': field_values
        })


class EmployeeUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        field_values = {str(fv.form_field.id): fv.value for fv in employee.field_values.all()}
        
        return render(request, 'employees/employee_edit.html', {
            'employee': employee,
            'field_values': field_values
        })
    
    def post(self, request, pk):
        try:
            employee = get_object_or_404(Employee, pk=pk)
            data = json.loads(request.body)
            field_values = data.get('field_values', {})
            
            # Validate required fields
            for field in employee.form_template.fields.filter(required=True):
                if str(field.id) not in field_values or not field_values[str(field.id)]:
                    return JsonResponse({
                        'success': False, 
                        'message': f'{field.label} is required'
                    }, status=400)
            
            with transaction.atomic():
                # Update field values
                for field_id, value in field_values.items():
                    try:
                        form_field = FormField.objects.get(id=int(field_id))
                        EmployeeFieldValue.objects.update_or_create(
                            employee=employee,
                            form_field=form_field,
                            defaults={'value': value}
                        )
                    except FormField.DoesNotExist:
                        pass
            
            return JsonResponse({
                'success': True,
                'message': 'Employee updated successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class EmployeeDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        try:
            employee = get_object_or_404(Employee, pk=pk)
            employee.delete()
            return JsonResponse({'success': True, 'message': 'Employee deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
