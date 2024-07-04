from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters, mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AdminOnly
from .serializers import SignupSerializer
from .serializers import TokenSerializer
from .serializers import UserSerializer
from .constants import SUBJECT, FROM


User = get_user_model()


def response_ok(serializer):
    return Response(serializer.data, status=status.HTTP_200_OK)


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
            return response_ok(serializer)
        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(role=self.request.user.role, partial=True)
            return response_ok(serializer)


class SendConfirmationCodeViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    #http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        print('*' * 30)
        print('perform_create()')
        print('*' * 30)
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
def send_confirmation_code_0(request):
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
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
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
    return response_ok(serializer)


@api_view(['POST'])
def send_confirmation_code(request):
    """Create and send confirmation code."""
    """if 1:
        user, _ = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email']
        )"""
    """except Exception:
        serializer = SignupSerializer(
            data=request.data
        )
    else:
        serializer = SignupSerializer(
            user,
            data=request.data
        )"""
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
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
    return response_ok(serializer)


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
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            pass
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
