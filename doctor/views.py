import doctor
from core.models import Doctor, User
from doctor.serializers import DoctorSerializer, StateSerializer, EditDoctorSerializer, ImageSerializer
from core.serializers import UserSerializer
from core import serializers
from django.shortcuts import render
from rest_framework import fields, request, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import authentication

from rest_framework.fields import CurrentUserDefault
# from rest_framework_extensions.mixins import NestedViewSetMixins

import json

from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from core.serializers import AuthTokenSerializer
# from rest_framework.mixins import NestedViewSetMixins

from core.views import Edit_user

# Create your views here.
def set_user_is_doctor( user_id, value):    # Cambiar el is doctor
        # user.is_doctor = value
    user = User.objects.get(pk=user_id)
    data = {"is_doctor": value, 'name':user.get_item('name'), 'username':user.get_item('username'), 'email':user.get_item('email'), 'password': '11111'}
    print('is_doctor',user.is_doctor)
    is_doctor = {'is_doctor': value, }
    user.is_doctor = value
    user.save()
    return user

class DoctorViewSet(viewsets.ModelViewSet):
    
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    paginate_by = 4
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # self.objects.filter(author=user).order_by('-date_posted')
        # username=self.kwargs.get('username')
        
        return self.queryset.all()  # user=User.objects. get(pk=pk)


    def perform_create(self, serializer_class):    # no funciona, utilizar ruta create
        print('perform create')
        doctor = self.request.data
        #  request_user = self.request.user    # Poner el  usuario como doctor
        #  request_user['is_doctor'] = True
        #  doctor['user'] = request_user

        # Cambiar el is_doctor del usuario
        request_user = set_user_is_doctor(user=self.request.user, value=True)

        print('request_user', request_user)
        serializer_class = DoctorSerializer(data=doctor, user=request_user)
        if serializer_class.is_valid():
            serializer_class.save()
            return serializer_class
        return serializer_class

    
    def _params_to_ints(self, qs):
        # Convierte una cadena de parametros en cadena de enteros
        return [int(str_id) for str_id in qs.split(',')]
    
    # Filtrar doctors by speciality and doctor
    def get_queryset(self):
        specialitys = self.request.query_params.get('speciality')
        ubications =  self.request.query_params.get('ubication')
        queryset = self.queryset
        if specialitys:
            # for speciality in specialitys:
            #     print(speciality)
            queryset = queryset.filter(speciality=specialitys)  
   
        if ubications:
            queryset = queryset.filter(ubication=ubications)
   
        return queryset.filter()  

class LoginDoctor(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class CreateDoctorView(APIView):  # LoginRequiredMixin, UserPassesTestMixin, 
    authentication_classes = (authentication.TokenAuthentication,) 
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        doctor = self.request.data
        print('user', self.request.user)
        # user2= CurrentUserDefault()

        request_user = set_user_is_doctor(user_id=self.request.user.id, value=True)   # Set is_doctor=True
        print('request_user', request_user)
        doctor['user'] =  request_user.id  # self.request.user.id
        serializer = DoctorSerializer(data=doctor)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditDoctorList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditDoctorDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        doctor = self.get_object(pk)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StateDoctor(APIView):
    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = StateSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = StateSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditDoctor(APIView):
    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = EditDoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        doctor = self.get_object(pk)
        items = ['speciality', 'username', 'name']
        # doctor_dic = json.loads(doctor)  Convertir json to dic
        doctor_data = request.data
        # items_2 = doctor_data.keys()
        
        for item in items:
            if not doctor_data.get(item):
                doctor_data[item] = doctor.get_item(item)

        serializer = EditDoctorSerializer(doctor, data=doctor_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class ResponseImage(viewsets.ModelViewSet):  # NestedViewSetMixin,
# 
#     http_method_names = ['get', 'put']
#     queryset = Doctor.objects.all()
#     serializer_class = ImageSerializer
#     pagination_class = None
# 
#     def get_queryset(self, *args, **kwargs):
#         doctor = Doctor.objects.get(pk=pk)
#         filename = doctor.image
#         size = filename.size
#         response = FileResponse(open(filename.path, 'rb'), content_type="image/png")
#         response['Content-Length'] = size
#         response['Content-Disposition'] = "attachment; filename=%s" % 'notification-icon.png'
#         return response 


class ResponseImage(APIView):
    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        doctor = self.get_object(pk)
        filename = doctor.image
        size = filename.size
        response = FileResponse(open(filename.path, 'rb'), content_type="image/png")
        response['Content-Length'] = size
        response['Content-Disposition'] = "attachment; filename=%s" % 'notification-icon.png'
        return response 
