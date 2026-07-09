import os
from .models import Profile, Skill, Education, Experience, SavedJob, AppliedJob
from django.utils import timezone
from django.conf import settings

class ProfileRepository:
    @staticmethod
    def get_or_create_by_user(user_id):
        p, _ = Profile.objects.get_or_create(user_id=user_id)
        return p

    @staticmethod
    def save(profile):
        profile.save()
        return profile

class ResumeRepository:
    @staticmethod
    def save_resume(profile, file_obj, text):
        profile.resume_file = file_obj
        profile.resume_text = text
        profile.updated_at = timezone.now()
        profile.save()
        return profile

class JobActivityRepository:
    @staticmethod
    def save_job(profile, job_id):
        return SavedJob.objects.create(profile=profile, job_id=job_id)

    @staticmethod
    def apply_job(profile, job_id):
        return AppliedJob.objects.create(profile=profile, job_id=job_id)
