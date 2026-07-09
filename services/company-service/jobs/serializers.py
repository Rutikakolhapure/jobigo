from rest_framework import serializers
from .models import Job, Category, Location, Skill, JobSkill

class SkillSerializer(serializers.ModelSerializer):
    """Skill serializer."""
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'description', 'is_active']

class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon_url']

class LocationSerializer(serializers.ModelSerializer):
    """Location serializer."""
    class Meta:
        model = Location
        fields = ['id', 'city', 'state', 'country', 'country_code']

class JobSkillSerializer(serializers.ModelSerializer):
    """Job skill serializer."""
    skill_name = serializers.CharField(source='skill.name', read_only=True)

    class Meta:
        model = JobSkill
        fields = ['id', 'skill', 'skill_name', 'proficiency_level', 'years_required']

class JobSerializer(serializers.ModelSerializer):
    """Job serializer."""
    company_name = serializers.CharField(source='company.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    skills = JobSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'company', 'company_name', 'title', 'slug', 'description',
            'requirements', 'responsibilities', 'benefits', 'location',
            'location_type', 'salary_min', 'salary_max', 'experience_level',
            'employment_type', 'category', 'category_name', 'status', 'skills',
            'views_count', 'applications_count', 'deadline', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'views_count', 'applications_count', 'created_at', 'updated_at']
