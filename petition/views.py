from rest_framework.settings import perform_import
from rest_framework.views import APIView
from core.models import Petition, Doctor, Patient
from petition.serializers import PetitionSerializer
from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import authentication
from rest_framework.response import Response


class PetitionViewSet(viewsets.ModelViewSet):
    serializer_class = PetitionSerializer
    queryset = Petition.objects.all()

    def perform_create(self, serializer_class):     # utilizar metodo patch
        print('perform create')
        # petition = Petition.objects.all()
        serializer_class = PetitionSerializer(data = self.request.data) # petition
        if serializer_class.is_valid():
            serializer_class.save()
            return serializer_class
        return serializer_class
    

    def _params_to_ints(self, qs):
        # Convierte una cadena de parametros en cadena de enteros
        return [int(str_id) for str_id in qs.split(',')]
    
    # Filtrar doctors by speciality and doctor
    def get_queryset(self):
        specialitys = self.request.query_params.get('doctor')
        ubications =  self.request.query_params.get('patient')
        queryset = self.queryset
        if specialitys:
            # for speciality in specialitys:
            #     print(speciality)
            queryset = queryset.filter(speciality=specialitys)  
   
        if ubications:
            queryset = queryset.filter(ubication=ubications)
   
        return queryset.filter()  

class FindPetitionUser(APIView):
    authentication_classes = (authentication.TokenAuthentication,) 
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        usuario = self.request.user
        print('usuario', usuario.is_doctor)
        if usuario.is_doctor:
            doctor_in = Doctor.objects.get(pk=usuario.id)
            petitions = Petition.objects.filter(doctor=doctor_in)
            serializer = PetitionSerializer(petitions, many=True)
            return Response(serializer.data)

        else:
            print('usuario id ', usuario.id)
            patient_in = Patient.objects.get(user=usuario)
            print('patient_in', patient_in)
            petitions = Petition.objects.filter(patient=patient_in)
            serializer = PetitionSerializer(petitions, many=True)
            return Response(serializer.data)

