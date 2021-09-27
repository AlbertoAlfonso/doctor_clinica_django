from django.shortcuts import render
from django.contrib.auth import get_user, get_user_model, authenticate
from core.models import Patient
from patient.serializers import UserSerializer, PatientSerializer, PatientDetailSerializer
from core.serializers import AuthTokenSerializer

from rest_framework import generics, authtoken, permissions
from rest_framework import viewsets, filters

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import authentication
 

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from doctor.views import set_user_is_doctor


class CreatePatientView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    authentication_classes = (authentication.TokenAuthentication,) 
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        request_user = set_user_is_doctor(user_id=self.request.user.id, value=False)   # Set is_doctor=True
        print('perform create')
        serializer.save()  # user = self.request.user

class CreatetokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientDetailSerializer
    # authentication_classes = (authentication.TokenAuthentication,) 
    # permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Patient.objects.get(pk=2)

class UserListViewSet(viewsets.ModelViewSet):
    # Crear y actualizar perfiles
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOurProfile,)
    # permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    searchfields =('username', 'email')


