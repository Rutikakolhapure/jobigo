from django.contrib import admin
from .models import CandidateProfile, Education, Experience, Resume, Skill

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'headline', 'location', 'years_of_experience', 'profile_completion_percentage', 'created_at')
    list_filter = ('is_open_to_opportunities', 'created_at')
    search_fields = ('headline', 'location', 'user_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'degree', 'field_of_study', 'start_date', 'is_current')
    list_filter = ('is_current', 'start_date')
    search_fields = ('school_name', 'field_of_study')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'start_date', 'is_current', 'employment_type')
    list_filter = ('is_current', 'start_date')
    search_fields = ('job_title', 'company_name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'profile', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('file_name', 'profile__user_id')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'profile', 'proficiency_level', 'years_of_experience', 'endorsements_count')
    list_filter = ('proficiency_level',)
    search_fields = ('skill_name', 'profile__user_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
