from django.shortcuts import render
from django.contrib.auth import get_user, get_user_model, authenticate
from rest_framework.views import APIView
from core.models import Patient, User
from patient.serializers import UserSerializer, PatientSerializer, PatientDetailSerializer
from core.serializers import AuthTokenSerializer

from rest_framework import generics, authtoken, permissions
from rest_framework import viewsets, filters

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.response import Response
from rest_framework import status

from rest_framework.pagination import PageNumberPagination


class CreateUserView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # pagination_by = 5
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def perform_create(self, serializer):
        serializer.save()  # user = self.request.user

class CreatetokenView(ObtainAuthToken):                     # Arreglar para crear usuarios no pacientes
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserListViewSet(viewsets.ModelViewSet):
    # Crear y actualizar perfiles
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOurProfile,)
    # permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    searchfields =('username', 'email')

class Edit_user(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise User

    def get(self, request, pk, form=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        items = ['name', 'email', 'username', 'is_doctor']
        # doctor_dic = json.loads(doctor)  Convertir json to dic
        user_data = request.data

        is_doctor = user_data.get('is_doctor')
        print('request', user_data.get('is_doctor'))
        # items_2 = doctor_data.keys()
        if not user_data.get('password'):
            user_data['password'] = '11111'

        for item in items:
            if not user_data.get(item):
                user_data[item] = user.get_item(item)

        if user_data['is_doctor']:        # Sobre escribir el valor de is_doctor ya que en la condicion anterior no ve la diferencia entre el false y empty
            print("if false")
            if is_doctor == False:
                user_data['is_doctor'] = False
        print(user_data)

        serializer = UserSerializer(user, data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)