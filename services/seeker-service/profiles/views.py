from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CandidateProfile, Education, Experience, Resume, Skill
from .serializers import CandidateProfileSerializer, EducationSerializer, ExperienceSerializer, ResumeSerializer, SkillSerializer
import logging

logger = logging.getLogger(__name__)

class CandidateProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for candidate profiles."""

    queryset = CandidateProfile.objects.filter(deleted_at__isnull=True)
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['location', 'is_open_to_opportunities']
    search_fields = ['headline', 'location']
    ordering = ['-created_at']

    def get_object(self):
        """Get profile for current user."""
        obj, created = CandidateProfile.objects.get_or_create(user_id=self.request.user.id)
        return obj

    @action(detail=False, methods=['get', 'put'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get or update current user's profile."""
        profile, created = CandidateProfile.objects.get_or_create(user_id=request.user.id)
        if request.method == 'PUT':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

class EducationViewSet(viewsets.ModelViewSet):
    """ViewSet for education."""

    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-start_date']

    def get_queryset(self):
        profile = CandidateProfile.objects.filter(user_id=self.request.user.id).first()
        if profile:
            return Education.objects.filter(profile=profile)
        return Education.objects.none()

    def perform_create(self, serializer):
        profile, created = CandidateProfile.objects.get_or_create(user_id=self.request.user.id)
        serializer.save(profile=profile)

class ExperienceViewSet(viewsets.ModelViewSet):
    """ViewSet for work experience."""

    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-start_date']

    def get_queryset(self):
        profile = CandidateProfile.objects.filter(user_id=self.request.user.id).first()
        if profile:
            return Experience.objects.filter(profile=profile)
        return Experience.objects.none()

    def perform_create(self, serializer):
        profile, created = CandidateProfile.objects.get_or_create(user_id=self.request.user.id)
        serializer.save(profile=profile)

class ResomeViewSet(viewsets.ModelViewSet):
    """ViewSet for resumes."""

    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-created_at']

    def get_queryset(self):
        profile = CandidateProfile.objects.filter(user_id=self.request.user.id).first()
        if profile:
            return Resume.objects.filter(profile=profile)
        return Resume.objects.none()

    def perform_create(self, serializer):
        profile, created = CandidateProfile.objects.get_or_create(user_id=self.request.user.id)
        serializer.save(profile=profile)
