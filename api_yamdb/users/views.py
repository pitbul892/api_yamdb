from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer
from .serializers import TokenSerializer
from .serializers import UsersSerializer
from .serializers import UsersMeSerializer
from .permissions import RoleAdminOrSuperuserOnly
from .serializers import (SignupSerializer, TokenSerializer,
                          UsersMeSerializer, UsersSerializer)
from .serializers import PatchUserSerializer

SUBJECT = 'Your confirmation code'
FROM = 'no-reply@example.com'

User = get_user_model()


def create_confirmation_code(user):
    return default_token_generator.make_token(user)


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }


@api_view(['POST'])
def send_confirmation_code(request):
    """Create and send confirmation code."""
    try:
        user = User.objects.get(
            username=request.data['username'],
            email=request.data['email']
        )
    except Exception:
        serializer = SignupSerializer(
            data=request.data
        )
    else:
        serializer = SignupSerializer(
            user,
            data=request.data
        )
    if serializer.is_valid():
        if request.data['username'] == 'me':
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = User.objects.get(
            username=request.data['username']
        )
        confirmation_code = create_confirmation_code(user)
        send_mail(
            subject=SUBJECT,
            message=confirmation_code,
            from_email=FROM,
            recipient_list=[request.data['email']],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_token(request):
    """Create token for auth user."""
    if 'username' in request.data:
        user = get_object_or_404(
            User,
            username=request.data['username'],
        )
        try:
            serializer = TokenSerializer(user, data=request.data)
            confirmation_code = request.data['confirmation_code']
            if default_token_generator.check_token(
                user,
                confirmation_code
            ):
                if serializer.is_valid():
                    token = get_token_for_user(user)
                    return Response(token, status=status.HTTP_200_OK)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            pass
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


def is_valid(serializer):
    """Check if serializer iz valid."""
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                serializer.data, status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def username_endpoint(request, username):
    """View-function for 'username/' endpoint."""
    if request.auth:
        if request.user.is_admin:
            try:
                user = User.objects.get(username=username)
            except Exception:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = UsersSerializer(user)
                if request.method == 'GET':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                if request.method == 'DELETE':
                    user.delete()
                    return Response({}, status=status.HTTP_204_NO_CONTENT)
                if request.method == 'PATCH':
                    serializer = PatchUserSerializer(
                        user,
                        data=request.data,
                        partial=True
                    )
                    return is_valid(serializer)
        return Response({}, status=status.HTTP_403_FORBIDDEN)
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class UserListCreateView(generics.ListCreateAPIView):
    """Viewset for 'user/' endpoint."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        RoleAdminOrSuperuserOnly
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


@api_view(['GET', 'PATCH'])
def me(request):
    """View-function for 'me/' endpoint."""
    if request.auth:
        try:
            user = User.objects.get(pk=request.user.id)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        else:
            if request.method == 'GET':
                serializer = UsersMeSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'PATCH':
                serializer = UsersMeSerializer(
                    user,
                    data=request.data,
                    partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
