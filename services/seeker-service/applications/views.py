from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobApplication, SavedJob
from .serializers import JobApplicationSerializer, SavedJobSerializer
import logging

logger = logging.getLogger(__name__)

class JobApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for job applications."""

    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'job_id']
    search_fields = ['job_id']
    ordering = ['-applied_at']

    def get_queryset(self):
        return JobApplication.objects.filter(candidate_id=self.request.user.id, deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(candidate_id=self.request.user.id)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update application status."""
        application = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(JobApplication.Status.choices):
            return Response({'error': 'Invalid status'}, status=400)
        
        application.status = new_status
        application.save()
        serializer = self.get_serializer(application)
        return Response(serializer.data)

class SavedJobViewSet(viewsets.ModelViewSet):
    """ViewSet for saved jobs."""

    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-saved_at']

    def get_queryset(self):
        return SavedJob.objects.filter(candidate_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(candidate_id=self.request.user.id)
