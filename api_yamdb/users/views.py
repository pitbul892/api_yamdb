from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer
from .serializers import TokenSerializer
from .serializers import UsersSerializer
from .permissions import AdminOnly
from .serializers import SignupSerializer, TokenSerializer
from .serializers import UserSerializer, UsersSerializer
from .constants import SUBJECT, FROM


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for users/ and users/me/ endpoints."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (
        permissions.IsAuthenticated,
        AdminOnly
    )

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(role=self.request.user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if request.method == 'PUT':
            return Response(serializer.initial_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


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
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.get(
            username=request.data['username']
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject=SUBJECT,
            message=confirmation_code,
            from_email=FROM,
            recipient_list=[request.data['email']],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


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
                    refresh = RefreshToken.for_user(user)
                    token = {'token': str(refresh.access_token)}
                    return Response(token, status=status.HTTP_200_OK)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            pass
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(generics.ListCreateAPIView):
    """Viewset for 'user/' endpoint."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        AdminOnly
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
