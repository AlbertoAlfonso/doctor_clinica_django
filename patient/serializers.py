from django.db.models.query import QuerySet
from core.models import Doctor, Patient, User
from rest_framework import serializers
from django.db.models import fields
from django.contrib.auth import get_user, get_user_model, authenticate
from django.utils.translation import ungettext_lazy as _  # metodo de traduccion
from core.serializers import UserSerializer

class PatientSerializer(serializers.ModelSerializer):
    # user = UserSerializer()  # read_only=True
    user = serializers.PrimaryKeyRelatedField(
        queryset= get_user_model().objects.all(),
        many=False)
    username = serializers.CharField(read_only=True, source="user.username")
    is_doctor = serializers.BooleanField(read_only=True, source="user.is_doctor")
    doctor = serializers.PrimaryKeyRelatedField(  # RelatedField
        queryset = Doctor.objects.all(),
        many= False
    )
    class Meta:
        model = Patient
        fields = ['id', 'sick', 'name', 'username', 'user', 'is_doctor', 'doctor']
        read_only_fields = ['id']

class PatientDetailSerializer(PatientSerializer):
    user = UserSerializer(read_only=True)