from core.models import Patient, User
from rest_framework import serializers
from django.db.models import fields
from django.contrib.auth import get_user, get_user_model, authenticate
from django.utils.translation import ungettext_lazy as _  # metodo de traduccion

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'name', 'is_doctor')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        
        return get_user_model().objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
    #     print('validate data', validated_data)
    #     password = validated_data.pop('password', None)
    #     user = super().update(instance, **validated_data)
# 
    #     if password:
    #         user.set_password(password)
    #         user.save()
# 
    #     return user

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        print(validated_data)
        instance.username = validated_data.get('username', instance.username)  # First complete de fields of instance 
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_doctor = validated_data.get('is_doctor', instance.is_doctor)
        instance.save()

        if password and password !='11111':
            instance.set_password(password)
            instance.save()

        return instance

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username = username,
            password = password
        )

        if not user:
            msg = _('Unableto authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

