from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from companies.views import CompanyViewSet
from jobs.views import JobViewSet, CategoryViewSet, LocationViewSet, SkillViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'skills', SkillViewSet, basename='skill')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company/', include(router.urls)),
]
