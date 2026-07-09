from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    """Company serializer."""

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description', 'website', 'logo_url', 'cover_image_url',
            'email', 'phone', 'industry', 'company_size', 'founded_year',
            'headquarters', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
