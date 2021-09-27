from django.urls import path
from django.urls.conf import include
from patient import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('user_list', views.UserListViewSet, basename='user-list')


app_name = 'patient'
urlpatterns = [
    path('create', views.CreatePatientView.as_view(), name='create'),
    path('token', views.CreatetokenView.as_view(), name='token'),
    path('me', views.ManageUserView.as_view(), name='me'),
    path('', include(router.urls))
]