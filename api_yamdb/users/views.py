from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AdminOnly
from .serializers import (
    SignupSerializer,
    TokenSerializer,
    UserSerializer
)
from .constants import SUBJECT, FROM


User = get_user_model()


def response_200(serializer):
    """Return HTTP_200_OK response."""
    return Response(serializer.data, status=status.HTTP_200_OK)

def response_400(serializer=None):
    """Return HTTP_400_BAD_REQUEST response."""
    if serializer:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


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
    http_method_names = ['patch', 'get', 'post', 'delete']

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return response_200(serializer)
        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(role=self.request.user.role, partial=True)
            return response_200(serializer)


class SendConfirmationCodeViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for users/signup/ endpoint."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.get(
            username=self.request.data['username']
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject=SUBJECT,
            message=confirmation_code,
            from_email=FROM,
            recipient_list=[self.request.data['email']],
            fail_silently=True,
    )


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
                if serializer.is_valid(raise_exception=True):
                    refresh = RefreshToken.for_user(user)
                    token = {'token': str(refresh.access_token)}
                    return Response(token, status=status.HTTP_200_OK)
                return response_400(serializer)
        except Exception:
            pass
    return response_400()
