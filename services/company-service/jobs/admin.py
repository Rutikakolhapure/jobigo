from django.contrib import admin
from .models import Job, Category, Location, Skill, JobSkill

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Admin for Job model."""
    list_display = ('title', 'company', 'status', 'experience_level', 'applications_count', 'created_at')
    list_filter = ('status', 'experience_level', 'location_type', 'created_at')
    search_fields = ('title', 'company__name', 'description')
    readonly_fields = ('id', 'slug', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model."""
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin for Location model."""
    list_display = ('city', 'state', 'country')
    list_filter = ('country',)
    search_fields = ('city', 'country')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin for Skill model."""
    list_display = ('name', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'category')

@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    """Admin for JobSkill model."""
    list_display = ('job', 'skill', 'proficiency_level', 'years_required')
    list_filter = ('proficiency_level',)
    search_fields = ('job__title', 'skill__name')
