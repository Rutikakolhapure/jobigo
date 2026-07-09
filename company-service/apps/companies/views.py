from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Company, Job
from .serializers import CompanySerializer, JobListSerializer, JobDetailSerializer
from .repositories import JobRepository
from django.shortcuts import get_object_or_404
from django.conf import settings

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

class JobViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        q = request.query_params.get('q')
        category = request.query_params.get('category')
        location = request.query_params.get('location')
        skill = request.query_params.get('skill')
        employment_type = request.query_params.get('employment_type')
        remote = request.query_params.get('remote')
        salary_min = request.query_params.get('salary_min')
        salary_max = request.query_params.get('salary_max')

        remote_bool = None
        if remote is not None:
            remote_bool = remote.lower() in ['1', 'true', 'yes']

        jobs = JobRepository.search_jobs(q=q, category_id=category, location_id=location, skill_id=skill, employment_type=employment_type, remote=remote_bool, salary_min=salary_min, salary_max=salary_max)
        # ordering and pagination handled by DRF if wrapped in GenericViewSet; here simple list
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        job = get_object_or_404(Job, pk=pk)
        serializer = JobDetailSerializer(job)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_job(self, request):
        # Recruiter-only enforcement should be handled by gateway/auth; here we assume user is recruiter
        data = request.data.copy()
        company_id = data.pop('company_id', None)
        if not company_id:
            return Response({'detail': 'company_id required'}, status=status.HTTP_400_BAD_REQUEST)
        company = get_object_or_404(Company, pk=company_id)
        serializer = JobDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        job = Job.objects.create(company=company, **serializer.validated_data)
        return Response(JobDetailSerializer(job).data, status=status.HTTP_201_CREATED)
