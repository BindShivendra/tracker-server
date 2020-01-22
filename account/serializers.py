from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions
from django.contrib.auth import password_validation as validators
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404

from .models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [  'email', 'slug', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active' ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password', 'password1']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError('Passwords do not match')
        return super(UserRegisterSerializer, self).validate(attrs)

    def create(self, validated_data):
        # validated_data {'email': 'shiv@email.com', 'first_name': 'Shiv', 'last_name': 'bind', 'password': 'sssss', 'password2': 'sssssss'}
        email=validated_data['email']
        first_name=validated_data.get('first_name', '')
        last_name=validated_data.get('last_name', '')
        password=validated_data['password']
        user = CustomUser(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return  user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class UserPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True) 
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email','old_password', 'new_password', 'confirm_password']
        extra_kwargs = {
            'email': {'read_only': True},
        }

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError('Old password do not match')
        print('old opass')
        return value

    def validate(self, attrs):
        password = attrs['new_password']
        try:
            validators.validate_password(password=password, user=self.instance)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')

        return super(UserPasswordSerializer, self).validate(attrs)


    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()
        return instance

class GetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            validate_email(email)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        password = attrs.get('password')

        if email and password:
            user =  get_object_or_404(CustomUser, email=email)
            auth_user = authenticate(email=email, password=password)
        else:
            raise serializers.ValidationError('Email or password is not proveded')

        if auth_user:
            if not auth_user.is_active:
                raise serializers.ValidationError('User account is desables')
        else:
            raise serializers.ValidationError('Email or password is not correct')
        
        return super(GetTokenSerializer, self).validate(attrs)

