from rest_framework import serializers
from django.db import transaction
from .models import FormTemplate, FormField


class FormFieldSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FormField
        fields = ['id', 'label', 'field_type', 'placeholder', 'options', 'required', 'order']


class FormTemplateSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = FormTemplate
        fields = ['id', 'name', 'description', 'fields', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class FormTemplateCreateSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)
    
    class Meta:
        model = FormTemplate
        fields = ['id', 'name', 'description', 'fields']
    
    @transaction.atomic
    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        form_template = FormTemplate.objects.create(**validated_data)
        
        for field_data in fields_data:
            FormField.objects.create(form_template=form_template, **field_data)
        
        return form_template
    
    @transaction.atomic
    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', [])
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        # Delete existing fields and recreate
        instance.fields.all().delete()
        for field_data in fields_data:
            FormField.objects.create(form_template=instance, **field_data)
        
        return instance
