from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, JobsActivityViewSet

router = DefaultRouter()

urlpatterns = [
    path('profile/', ProfileViewSet.as_view({'get': 'retrieve'})),
    path('profile/upload-resume/', ProfileViewSet.as_view({'post': 'upload_resume'})),
    path('jobs/save/', JobsActivityViewSet.as_view({'post': 'save_job'})),
    path('jobs/apply/', JobsActivityViewSet.as_view({'post': 'apply_job'})),
]
