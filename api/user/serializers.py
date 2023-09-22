from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from apps.account.models import Account


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'role', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': 'Password did not match, please try again'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=68, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        email = obj.get('email')
        tokens = Account.objects.get(email=email).tokens
        return tokens

    class Meta:
        model = Account
        fields = ('email', 'tokens', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed({
                'message': 'email or password is not correct'
            })
        if not user.is_active:
            raise AuthenticationFailed({
                'message': 'Account disabled'
            })

        data = {
            'email': user.email,
        }
        return data


class AccountUpdateSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)

    def get_role(self, obj):
        return obj.get_role_display()

    class Meta:
        model = Account
        fields = ('id', 'full_name', 'username', 'image_url', 'email', 'phone', 'role')


class AccountOwnImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('image',)


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)

    class Meta:
        model = Account
        fields = ('password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context['request']
        user = request.user
        current_password = user.password
        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': 'Password did not match, '
                                                                            'please try again new'})

        if check_password(password, current_password):
            raise serializers.ValidationError(
                {'success': False, 'message': 'New password should not similar to current password'})

        user.set_password(password)
        user.save()
        return attrs