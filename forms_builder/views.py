from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
import json

from .models import FormTemplate, FormField


class FormTemplateListView(LoginRequiredMixin, View):
    
    def get(self, request):
        form_templates = FormTemplate.objects.all()
        return render(request, 'forms_builder/form_list.html', {'form_templates': form_templates})


class FormTemplateCreateView(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request, 'forms_builder/form_create.html')
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description', '')
            fields = data.get('fields', [])
            
            if not name:
                return JsonResponse({'success': False, 'message': 'Form name is required'}, status=400)
            
            with transaction.atomic():
                # Create form template
                form_template = FormTemplate.objects.create(
                    name=name,
                    description=description,
                    created_by=request.user
                )
                
                # Create fields
                for i, field in enumerate(fields):
                    FormField.objects.create(
                        form_template=form_template,
                        label=field.get('label', ''),
                        field_type=field.get('field_type', 'text'),
                        placeholder=field.get('placeholder', ''),
                        options=field.get('options'),
                        required=field.get('required', False),
                        order=i
                    )
            
            return JsonResponse({
                'success': True,
                'message': 'Form template created successfully',
                'id': form_template.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class FormTemplateDetailView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        form_template = get_object_or_404(FormTemplate, pk=pk)
        
        if request.headers.get('Accept') == 'application/json':
            fields = [{
                'id': f.id,
                'label': f.label,
                'field_type': f.field_type,
                'placeholder': f.placeholder,
                'options': f.options,
                'required': f.required,
                'order': f.order
            } for f in form_template.fields.all()]
            
            return JsonResponse({
                'id': form_template.id,
                'name': form_template.name,
                'description': form_template.description,
                'fields': fields
            })
        
        return render(request, 'forms_builder/form_detail.html', {'form_template': form_template})


class FormTemplateUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        form_template = get_object_or_404(FormTemplate, pk=pk)
        # Serialize fields to JSON for JavaScript
        fields_json = json.dumps([{
            'id': f.id,
            'label': f.label,
            'field_type': f.field_type,
            'required': f.required,
            'options': f.options
        } for f in form_template.fields.all()])
        return render(request, 'forms_builder/form_edit.html', {
            'form_template': form_template,
            'fields_json': fields_json
        })
    
    def post(self, request, pk):
        try:
            form_template = get_object_or_404(FormTemplate, pk=pk)
            data = json.loads(request.body)
            
            with transaction.atomic():
                form_template.name = data.get('name', form_template.name)
                form_template.description = data.get('description', form_template.description)
                form_template.save()
                
                # Update fields
                fields = data.get('fields', [])
                form_template.fields.all().delete()
                
                for i, field in enumerate(fields):
                    FormField.objects.create(
                        form_template=form_template,
                        label=field.get('label', ''),
                        field_type=field.get('field_type', 'text'),
                        placeholder=field.get('placeholder', ''),
                        options=field.get('options'),
                        required=field.get('required', False),
                        order=i
                    )
            
            return JsonResponse({
                'success': True,
                'message': 'Form template updated successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class FormTemplateDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        try:
            form_template = get_object_or_404(FormTemplate, pk=pk)
            form_template.delete()
            return JsonResponse({'success': True, 'message': 'Form template deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
