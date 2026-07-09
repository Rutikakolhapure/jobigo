from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegistrationSerializer, UserSerializer, ChangePasswordSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, EmailVerificationSerializer
from .repositories import UserRepository
from .services import send_verification_email, send_password_reset_email, verify_token
from django.contrib.auth.hashers import make_password

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Optionally set inactive until email verified
        user.is_active = True  # if you want verify-> set False and call send_verification_email
        user.save()
        send_verification_email(user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        # Delegate to SimpleJWT token view for token obtain
        return TokenObtainPairView.as_view()(request._request)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        return TokenRefreshView.as_view()(request._request)

    @action(detail=False, methods=['post'])
    def request_password_reset(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = UserRepository.get_by_email(email)
        if user:
            send_password_reset_email(user)
        # Always return ok to avoid leaking email existence
        return Response({'status': 'ok'})

    @action(detail=False, methods=['post'])
    def confirm_password_reset(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        payload = verify_token(token)
        if not payload:
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        user = UserRepository.get_by_id(payload.get('user_id'))
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(new_password)
        UserRepository.save(user)
        return Response({'status': 'ok'})

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': 'Old password incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'status': 'ok'})

    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        payload = verify_token(token)
        if not payload:
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        user = UserRepository.get_by_id(payload.get('user_id'))
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.is_active = True
        user.save()
        return Response({'status': 'ok'})

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
