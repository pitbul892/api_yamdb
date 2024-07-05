from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

from .constants import MAX_LENGTH_USERNAME
from .constants import MAX_LENGTH_EMAIL
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


class SignupSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except Exception:
            pass
        else:
            if user.username != data['username']:
                raise serializers.ValidationError(
                    'The email already exists!')
        try:
            user = User.objects.get(username=data['username'])
        except Exception:
            pass
        else:
            if user.email != data['email']:
                raise serializers.ValidationError(
                    'The username already exists!')
        return data

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
        except Exception:
            user, _ = User.objects.get_or_create(
                username=validated_data['username'],
                email=validated_data['email']
            )
        else:
            if user.username == validated_data['username']:
                return user

        # user, _ = User.objects.get_or_create(**validated_data)
        return user


class TokenSerializer(serializers.Serializer):
    """Serializer for token."""
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=[
            UnicodeUsernameValidator()
        ]
    )
    confirmation_code = serializers.CharField(required=True)
