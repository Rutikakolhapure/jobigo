from rest_framework import serializers
from .models import JobApplication, SavedJob

class JobApplicationSerializer(serializers.ModelSerializer):
    """Job application serializer."""

    class Meta:
        model = JobApplication
        fields = [
            'id', 'job_id', 'candidate_id', 'cover_letter', 'resume_url',
            'status', 'applied_at', 'viewed_at', 'rejected_at', 'updated_at'
        ]
        read_only_fields = ['id', 'applied_at', 'updated_at']

class SavedJobSerializer(serializers.ModelSerializer):
    """Saved job serializer."""

    class Meta:
        model = SavedJob
        fields = ['id', 'job_id', 'candidate_id', 'saved_at']
        read_only_fields = ['id', 'saved_at']
