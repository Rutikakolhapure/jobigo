from rest_framework import serializers
from .models import Profile, Skill, Education, Experience, SavedJob, AppliedJob

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'degree', 'start_date', 'end_date', 'description']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'company', 'title', 'start_date', 'end_date', 'description']

class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'headline', 'summary', 'location', 'photo', 'skills', 'resume_file', 'resume_text', 'profile_completion', 'educations', 'experiences', 'created_at']
        read_only_fields = ['profile_completion', 'resume_text', 'created_at']

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = ['id', 'job_id', 'saved_at']

class AppliedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedJob
        fields = ['id', 'job_id', 'applied_at', 'status']
