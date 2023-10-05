"""
Serializers for the user API View
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    USER_ROLE_CHOICES = (
        ('ST', 'Student'),
        ('RS', 'Researcher'),
        ('AM', 'Admin'),
        ('IS', 'Instructor'),
        ('MT', 'MTurker')
    )

    user_id = serializers.UUIDField(required=False, format='hex_verbose')
    utorid = serializers.CharField(required=False, max_length=10)
    user_role = serializers.ChoiceField(required=False, choices=USER_ROLE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ['user_id', 'name', 'password', 'utorid', 'user_role']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def validate_user_id(self, value):
        """
        Validate the user_id, ensuring it is unique.
        """
        UserModel = get_user_model()
        try:
            UserModel.objects.get(user_id=value)
            raise serializers.ValidationError("User with this User ID already exists.")
        except UserModel.DoesNotExist:
            return value

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""

    user_id = serializers.UUIDField(format='hex_verbose')
    name = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        user_id = attrs.get('user_id')
        name = attrs.get('name')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=user_id,
            password=password,
            name=name
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
