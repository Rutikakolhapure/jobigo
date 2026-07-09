from rest_framework import serializers
from .models import Company, Category, Location, Skill, Job

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'slug', 'website', 'logo', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city', 'region', 'country']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class JobListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'title', 'slug', 'company', 'employment_type', 'remote', 'salary_min', 'salary_max', 'currency', 'posted_at']

class JobDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'slug', 'company', 'description', 'categories', 'locations', 'skills', 'salary_min', 'salary_max', 'currency', 'employment_type', 'remote', 'visa_sponsorship', 'status', 'posted_at', 'expires_at']
