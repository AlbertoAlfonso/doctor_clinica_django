from core.models import Doctor, Patient, User
from rest_framework import serializers
from django.db.models import fields
from django.contrib.auth import get_user, get_user_model, authenticate
from django.utils.translation import ungettext_lazy as _  # metodo de traduccion
from core.serializers import UserSerializer

class DoctorSerializer(serializers.ModelSerializer):
    # user = UserSerializer()  # read_only=True
    user = serializers.PrimaryKeyRelatedField(  # RelatedField
        queryset= get_user_model().objects.all(),
        many=False)
    username = serializers.CharField(read_only=True, source="user.username")
    patients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    patient_name = serializers.ListField(read_only=True, source="patients.name")
    class Meta:
        model =Doctor
        fields = ['id', 'speciality', 'ubication', 'image', 'username', 'user', 'patient_name', 'patients']
        read_only_fields = ['id']

    # def save(self):
    #     print('save function', self)
    #     # user = self.context['request'].user
    #     user = self.validated_data['user']
    #     speciality = self.validated_data['speciality']
    #     ubication = self.validated_data['ubication']

    

class DoctorDetailSerializer(DoctorSerializer):
    user = UserSerializer(read_only=True)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('image')
        # read_only_fields = ['id']
        
class StateSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source="user.is_active")
    username = serializers.CharField(source="user.username")
    class Meta:
        model = Doctor
        fields = ['id', 'active', 'username']
        read_only_fields = ['id']

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user')
        user = instance.user

        instance.user = validated_data.get('user', instance.user)
        instance.save()

        user.is_active = user_data.get('is_active', user.is_active)
        user.username = user_data.get('username', user.username)
        user.save()

        return instance


class EditDoctorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    name = serializers.CharField(source="user.name")

    class Meta:
        model =Doctor
        fields = ['id', 'speciality', 'username', 'name']
        read_only_fields = ['id']

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user')    # user is a field of validated_data(doctor) 
        user = instance.user

        instance.user = validated_data.get('user', instance.user)  # First complete de fields of instance 
        instance.speciality = validated_data.get('speciality')
        instance.save()

        user.username = user_data.get('username', user.username)   # after complete fields of fields of instance
        user.name = user_data.get('name', user.name)
        user.save()

        return instance