from django.contrib.auth import get_user_model
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
            UnicodeUsernameValidator()
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
    """Serializer for username and email."""
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

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        return instance


class TokenSerializer(serializers.Serializer):
    """Serializer for username and email."""
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            UnicodeUsernameValidator()
        ]
    )

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        return instance
