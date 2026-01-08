from rest_framework import serializers
from django.db import transaction
from .models import Employee, EmployeeFieldValue
from forms_builder.serializers import FormTemplateSerializer


class EmployeeFieldValueSerializer(serializers.ModelSerializer):
    field_label = serializers.CharField(source='form_field.label', read_only=True)
    field_type = serializers.CharField(source='form_field.field_type', read_only=True)
    
    class Meta:
        model = EmployeeFieldValue
        fields = ['id', 'form_field', 'field_label', 'field_type', 'value']


class EmployeeSerializer(serializers.ModelSerializer):
    field_values = EmployeeFieldValueSerializer(many=True, read_only=True)
    form_template_name = serializers.CharField(source='form_template.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'form_template', 'form_template_name', 'field_values', 
                  'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class EmployeeCreateSerializer(serializers.Serializer):
    form_template = serializers.IntegerField()
    field_values = serializers.DictField(child=serializers.CharField(allow_blank=True))
    
    @transaction.atomic
    def create(self, validated_data):
        from forms_builder.models import FormTemplate, FormField
        
        form_template_id = validated_data['form_template']
        field_values_data = validated_data['field_values']
        created_by = validated_data['created_by']
        
        form_template = FormTemplate.objects.get(id=form_template_id)
        
        employee = Employee.objects.create(
            form_template=form_template,
            created_by=created_by
        )
        
        for field_id, value in field_values_data.items():
            try:
                form_field = FormField.objects.get(id=int(field_id))
                EmployeeFieldValue.objects.create(
                    employee=employee,
                    form_field=form_field,
                    value=value
                )
            except FormField.DoesNotExist:
                pass
        
        return employee
    
    @transaction.atomic
    def update(self, instance, validated_data):
        from forms_builder.models import FormField
        
        field_values_data = validated_data.get('field_values', {})
        
        # Update field values
        for field_id, value in field_values_data.items():
            try:
                form_field = FormField.objects.get(id=int(field_id))
                EmployeeFieldValue.objects.update_or_create(
                    employee=instance,
                    form_field=form_field,
                    defaults={'value': value}
                )
            except FormField.DoesNotExist:
                pass
        
        instance.save()
        return instance
