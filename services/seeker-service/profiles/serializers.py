from rest_framework import serializers
from .models import CandidateProfile, Education, Experience, Resume, Skill

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school_name', 'field_of_study', 'degree', 'start_date', 'end_date', 'is_current', 'grade', 'description']
        read_only_fields = ['id']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'job_title', 'company_name', 'location', 'description', 'start_date', 'end_date', 'is_current', 'employment_type', 'industry']
        read_only_fields = ['id']

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file_name', 'file_url', 'file_size', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill_name', 'proficiency_level', 'years_of_experience', 'endorsements_count']
        read_only_fields = ['id', 'endorsements_count']

class CandidateProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    resumes = ResumeSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = CandidateProfile
        fields = [
            'id', 'user_id', 'headline', 'summary', 'location', 'profile_completion_percentage',
            'resume_url', 'portfolio_url', 'github_url', 'linkedin_url', 'website_url',
            'years_of_experience', 'current_job_title', 'current_company', 'is_open_to_opportunities',
            'education', 'experience', 'resumes', 'skills', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'profile_completion_percentage', 'created_at', 'updated_at']
