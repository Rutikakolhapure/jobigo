from django.contrib import admin
from .models import Profile, Skill, Education, Experience, SavedJob, AppliedJob

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'headline', 'location', 'profile_completion')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'institution')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company', 'title')

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('profile', 'job_id', 'saved_at')

@admin.register(AppliedJob)
class AppliedJobAdmin(admin.ModelAdmin):
    list_display = ('profile', 'job_id', 'applied_at', 'status')
