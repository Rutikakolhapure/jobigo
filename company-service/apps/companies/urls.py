from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, JobViewSet

router = DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')

urlpatterns = router.urls
urlpatterns += [
    path('jobs/', JobViewSet.as_view({'get': 'list', 'post': 'create_job'})),
    path('jobs/<uuid:pk>/', JobViewSet.as_view({'get': 'retrieve'})),
]
