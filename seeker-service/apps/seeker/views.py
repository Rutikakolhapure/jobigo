from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProfileSerializer, SavedJobSerializer, AppliedJobSerializer
from .repositories import ProfileRepository, ResumeRepository, JobActivityRepository
from .models import Profile, SavedJob, AppliedJob
from django.conf import settings
import os

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        # Retrieve by profile id or by user_id query param
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                profile = Profile.objects.get(user_id=user_id)
            except Profile.DoesNotExist:
                return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            profile = ProfileRepository.get_or_create_by_user(request.user.id) if hasattr(request, 'user') and request.user else None
            if profile is None:
                return Response({'detail': 'user not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_resume(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'detail': 'not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        profile = ProfileRepository.get_or_create_by_user(user_id)
        f = request.FILES.get('file')
        if not f:
            return Response({'detail': 'file required'}, status=status.HTTP_400_BAD_REQUEST)
        # size check
        if f.size > settings.MAX_RESUME_SIZE_MB * 1024 * 1024:
            return Response({'detail': 'file too large'}, status=status.HTTP_400_BAD_REQUEST)
        # save file
        profile.resume_file.save(f.name, f, save=True)
        file_path = profile.resume_file.path
        from .services import ResumeService
        text, summary = ResumeService.parse_resume(file_path)
        profile.resume_text = text
        profile.summary = summary if hasattr(profile, 'summary') else ''
        # update completion score
        profile.profile_completion = SeekerMetricsService.compute_completion(profile)
        profile.save()
        return Response(ProfileSerializer(profile).data)

class JobsActivityViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def save_job(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'detail': 'not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        profile = ProfileRepository.get_or_create_by_user(user_id)
        job_id = request.data.get('job_id')
        if not job_id:
            return Response({'detail': 'job_id required'}, status=status.HTTP_400_BAD_REQUEST)
        sj = JobActivityRepository.save_job(profile, job_id)
        return Response(SavedJobSerializer(sj).data)

    @action(detail=False, methods=['post'])
    def apply_job(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'detail': 'not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        profile = ProfileRepository.get_or_create_by_user(user_id)
        job_id = request.data.get('job_id')
        if not job_id:
            return Response({'detail': 'job_id required'}, status=status.HTTP_400_BAD_REQUEST)
        aj = JobActivityRepository.apply_job(profile, job_id)
        return Response(AppliedJobSerializer(aj).data)

# Simple metrics service
class SeekerMetricsService:
    @staticmethod
    def compute_completion(profile: Profile):
        score = 0
        if profile.summary:
            score += 20
        if profile.skills.exists():
            score += 20
        if profile.experiences.exists():
            score += 20
        if profile.educations.exists():
            score += 20
        if profile.resume_text:
            score += 20
        return min(score, 100)
