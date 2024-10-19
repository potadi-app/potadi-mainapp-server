import os
from .models import User
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.forms import PasswordResetForm
from dj_rest_auth.serializers import PasswordResetConfirmSerializer as _PasswordResetConfirmSerializer
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from rest_framework.exceptions import ValidationError

class UserDetailsSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'registration_method', 'avatar', 'is_active']
        read_only_fields = ['id', 'registration_method', 'is_active']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.avatar and instance.registration_method == 'email':
            representation['avatar'] = f"{os.getenv('SERVER_DOMAIN')}{instance.avatar.url}"
        elif instance.google_avatar_url:
            representation['avatar'] = instance.google_avatar_url

        return representation

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user
    
    def save(self, request):
        validated_data = self.validated_data
        user = self.create(validated_data)
        return user

class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None, subject_template_name=None,
             email_template_name=None, use_https=False, token_generator=None,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        subject_template_name = 'registration/password_reset_subject.txt'
        email_template_name = 'registration/password_reset_email.html'
        html_email_template_name = 'registration/password_reset_email.html'
        return super().save(domain_override, subject_template_name,
                            email_template_name, use_https, token_generator,
                            from_email, request, html_email_template_name,
                            extra_email_context)

class CustomPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = CustomPasswordResetForm
    def get_email_options(self):
        return {
            'extra_email_context': {
                'CLIENT_DOMAIN': os.getenv('CLIENT_DOMAIN')
            }
        }

class PasswordResetConfirmSerializer(_PasswordResetConfirmSerializer):

    # Copy of parent class method with "if 'allauth'" taken out
    def validate(self, attrs):
        from allauth.account.forms import default_token_generator
        from django.utils.http import urlsafe_base64_decode as uid_decoder

        # Decode the uidb64 (allauth use base36) to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': [_('Invalid value')]})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': [_('Invalid value or link has expired')]})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs
    