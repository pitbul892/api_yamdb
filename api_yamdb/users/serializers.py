from django.contrib.auth import get_user_model
from rest_framework import serializers, validators


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """Serializer for username and email."""

    class Meta:
        model = User
        fields = ('username', 'email')


class UsersSerializer(serializers.ModelSerializer):
    """Serializer for users."""

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


class PatchUserSerializer(serializers.ModelSerializer):
    """Serializer to patch user."""

    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(max_length=254, required=True)

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

    def validate(self, data):
        if 'username' in data:
            if data['username'] == 'me':
                raise serializers.ValidationError(
                    'Используйте другой username!')
        return data


class UsersMeSerializer(serializers.ModelSerializer):
    """Serializer for users."""

    role = serializers.CharField(read_only=True)

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


class TokenSerializer(serializers.ModelSerializer):
    """Serializer for token."""

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )
