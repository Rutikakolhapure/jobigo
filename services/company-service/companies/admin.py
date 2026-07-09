from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin for Company model."""

    list_display = ('name', 'industry', 'company_size', 'is_verified', 'created_at')
    list_filter = ('company_size', 'is_verified', 'created_at')
    search_fields = ('name', 'industry')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
