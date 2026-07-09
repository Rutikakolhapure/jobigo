from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, ProfileViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

urlpatterns = [
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    path('request-password-reset/', AuthViewSet.as_view({'post': 'request_password_reset'}), name='request_password_reset'),
    path('confirm-password-reset/', AuthViewSet.as_view({'post': 'confirm_password_reset'}), name='confirm_password_reset'),
    path('verify-email/', AuthViewSet.as_view({'post': 'verify_email'}), name='verify_email'),
    path('profile/', ProfileViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='profile'),
]
