from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Category, Location, Skill, JobSkill
from .serializers import JobSerializer, CategorySerializer, LocationSerializer, SkillSerializer
import logging

logger = logging.getLogger(__name__)

class JobViewSet(viewsets.ModelViewSet):
    """ViewSet for job management."""

    queryset = Job.objects.filter(deleted_at__isnull=True, status='PUBLISHED')
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'experience_level', 'employment_type', 'location_type', 'company']
    search_fields = ['title', 'description', 'company__name']
    ordering_fields = ['created_at', 'salary_max', 'salary_min']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user.id)

    @action(detail=False, methods=['get'])
    def my_jobs(self, request):
        """Get jobs posted by current user."""
        jobs = self.queryset.filter(posted_by=request.user.id)
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        """Increment job views count."""
        job = self.get_object()
        job.views_count += 1
        job.save()
        return Response({'views_count': job.views_count})

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for job categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['name']
    ordering = ['name']

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for job locations."""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['country']
    search_fields = ['city', 'country']
    ordering = ['country', 'city']

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for skills."""

    queryset = Skill.objects.filter(is_active=True)
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['category']
    search_fields = ['name', 'category']
    ordering = ['name']
