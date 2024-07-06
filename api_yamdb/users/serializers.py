from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .constants import MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
from .validators import do_not_use_me


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users."""
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            UnicodeUsernameValidator(),
            do_not_use_me
        ]
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SignupSerializer(serializers.Serializer):
    """Serializer for sign up."""
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=[
            UnicodeUsernameValidator(),
            do_not_use_me
        ]
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        try:
            user, _ = User.objects.get_or_create(
                username=validated_data['username'],
                email=validated_data['email']
            )
        except Exception:
            raise serializers.ValidationError(
                'Please check your data!')
        return user


class TokenSerializer(serializers.Serializer):
    """Serializer for token."""
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=[
            UnicodeUsernameValidator(),
            do_not_use_me
        ]
    )
    confirmation_code = serializers.CharField(required=True)
