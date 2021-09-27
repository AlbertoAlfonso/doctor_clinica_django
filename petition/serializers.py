from django.db.models import fields, query
from django.db.models.base import Model
from rest_framework.relations import RelatedField
from core.models import Doctor, Patient, Petition
from rest_framework import serializers

class PetitionSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.user.username", read_only=True)
    patient_name = serializers.CharField(source="patient.user.username", read_only=True)
    
    patient = serializers.PrimaryKeyRelatedField(
        queryset = Patient.objects.all(),
    )
    class Meta:
        model = Petition
        fields =  '__all__'  # ['id', 'doctor', 'patient', 'title']
        read_only_fields = ['id']

    # def create(self, instance, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = instance.user
# 
    #     instance.user = validated_data.get('user', instance.user)
    #     instance.save()
# 
    #     user.is_active = user_data.get('is_active', user.is_active)
    #     user.username = user_data.get('username', user.username)
    #     user.save()

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