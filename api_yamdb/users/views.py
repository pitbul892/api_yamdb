import hashlib
import time
import base64

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer
from .serializers import TokenSerializer
from .serializers import UsersSerializer
from .serializers import UserMeSerializer


SUBJECT = 'Your confirmation code'
FROM = 'no-reply@example.com'

User = get_user_model()


def create_confirmation_code(data):
    m = hashlib.sha256()
    m.update(bytes(data, 'utf-8'))
    return base64.b64encode(m.digest()).decode('ascii')


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def send_confirmation_code(request):
    try:
        user = User.objects.get(
            username=request.data['username'],
            email=request.data['email']
        )
        print('user:', user)
    except Exception:
        serializer = SignupSerializer(data=request.data)
    else:
        serializer = SignupSerializer(user, data=request.data)
    if serializer.is_valid():
        if request.data['username'] == 'me':
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        message = request.data['username'] + str(time.time())
        confirmation_code = create_confirmation_code(message)
        serializer.validated_data['confirmation_code'] = confirmation_code
        serializer.save()
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
    if 'username' in request.data and 'confirmation_code' in request.data:
        try:
            user = User.objects.get(
                username=request.data['username'],
            )
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        else:
        
            try:
                serializer = TokenSerializer(user, data=request.data)
                if user.confirmation_code == request.data['confirmation_code']:
                    if serializer.is_valid():
                        token = get_token_for_user(user)
                        return Response(token, status=status.HTTP_200_OK)
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                pass
    return Response({}, status=status.HTTP_400_BAD_REQUEST)



class UsersViewSet(viewsets.ModelViewSet):
    """Viewset for users."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)


@api_view(['GET', 'PATCH'])
def me(request):
    try:
        user = User.objects.get(
            username=request.data['username']
        )
        print('user:', user)
    except Exception:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = UserMeSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
