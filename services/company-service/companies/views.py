from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
import logging

logger = logging.getLogger(__name__)

class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for company management."""

    queryset = Company.objects.filter(deleted_at__isnull=True)
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['industry', 'company_size', 'is_verified']
    search_fields = ['name', 'industry']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Set created_by to current user ID."""
        serializer.save(created_by=self.request.user.id)

    @action(detail=False, methods=['get'])
    def my_companies(self, request):
        """Get companies created by current user."""
        companies = self.queryset.filter(created_by=request.user.id)
        serializer = self.get_serializer(companies, many=True)
        return Response(serializer.data)
