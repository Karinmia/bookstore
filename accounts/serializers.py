from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import User


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'photo', 'affiliate_code')
        extra_kwargs = {'password': {'write_only': True}}


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    attrs['user'] = user
                else:
                    msg = 'User is deactivated.'
                    raise exceptions.ValidationError(msg)
            else:
                msg = 'Unable to login with given credentials.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide username and password both.'
            raise exceptions.ValidationError(msg)
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        validate_password(password)
        password2 = attrs.pop('password2', None)
        attrs['email'] = attrs.get('username')

        # Check if passwords match
        if password != password2:
            msg = 'Passwords not equal.'
            raise serializers.ValidationError(msg)

        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def validate(self, attrs):
        email = attrs.get('email', None)
        if email:
            attrs['username'] = email
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2')

    def validate_new_password(self, value):
        validate_password(value)
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        user = get_object_or_404(User, username=username)
        attrs['user'] = user
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'new_password2')

    def validate_new_password(self, value):
        validate_password(value)
        return value
