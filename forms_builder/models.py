from django.db import models
from django.conf import settings


class FormTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='form_templates'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'forms_builder_formtemplate'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class FormField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('date', 'Date'),
        ('textarea', 'Text Area'),
        ('select', 'Select/Dropdown'),
        ('checkbox', 'Checkbox'),
        ('file', 'File Upload'),
    ]
    
    form_template = models.ForeignKey(
        FormTemplate,
        on_delete=models.CASCADE,
        related_name='fields'
    )
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES, default='text')
    placeholder = models.CharField(max_length=255, blank=True, null=True)
    options = models.JSONField(
        blank=True, 
        null=True, 
        help_text='For select fields, store options as JSON array'
    )
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'forms_builder_formfield'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.label} ({self.field_type})"
