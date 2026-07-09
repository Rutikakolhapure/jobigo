from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from profiles.views import CandidateProfileViewSet, EducationViewSet, ExperienceViewSet, ResomeViewSet
from applications.views import JobApplicationViewSet, SavedJobViewSet

router = routers.DefaultRouter()
router.register(r'profiles', CandidateProfileViewSet, basename='profile')
router.register(r'education', EducationViewSet, basename='education')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'resumes', ResomeViewSet, basename='resume')
router.register(r'applications', JobApplicationViewSet, basename='application')
router.register(r'saved-jobs', SavedJobViewSet, basename='saved-job')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seeker/', include(router.urls)),
]
