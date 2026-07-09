from rest_framework import serializers

class CoverLetterRequestSerializer(serializers.Serializer):
    resume_text = serializers.CharField()
    job_description = serializers.CharField()
    skills = serializers.ListField(child=serializers.CharField(), required=False)

class CoverLetterResponseSerializer(serializers.Serializer):
    cover_letter = serializers.CharField()

class MatchRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    top_k = serializers.IntegerField(default=10)
