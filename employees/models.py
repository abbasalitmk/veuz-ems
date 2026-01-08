from django.db import models
from django.conf import settings
from forms_builder.models import FormTemplate, FormField


class Employee(models.Model):
    form_template = models.ForeignKey(
        FormTemplate,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employees_employee'
        ordering = ['-created_at']
    
    def __str__(self):
        # Try to get the first text field value as display name
        first_value = self.field_values.first()
        if first_value:
            return f"Employee #{self.id} - {first_value.value}"
        return f"Employee #{self.id}"
    
    def get_field_values_dict(self):
        return {fv.form_field.label: fv.value for fv in self.field_values.all()}


class EmployeeFieldValue(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='field_values'
    )
    form_field = models.ForeignKey(
        FormField,
        on_delete=models.CASCADE,
        related_name='employee_values'
    )
    value = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'employees_employeefieldvalue'
        unique_together = ['employee', 'form_field']
    
    def __str__(self):
        return f"{self.form_field.label}: {self.value}"
