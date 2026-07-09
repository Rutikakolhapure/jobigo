from django.contrib import admin
from .models import JobApplication, SavedJob

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate_id', 'job_id', 'status', 'applied_at', 'viewed_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('candidate_id', 'job_id')
    readonly_fields = ('id', 'applied_at', 'updated_at')
    ordering = ('-applied_at',)

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('candidate_id', 'job_id', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('candidate_id', 'job_id')
    readonly_fields = ('id', 'saved_at')
    ordering = ('-saved_at',)
