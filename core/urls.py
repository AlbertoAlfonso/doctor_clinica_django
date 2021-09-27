from django.urls import path
from django.urls.conf import include
from core import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('user_list', views.UserListViewSet, basename='user-list')


app_name = 'user'
urlpatterns = [
    path('create', views.CreateUserView.as_view(), name='create'),
    path('login', views.CreatetokenView.as_view(), name='core_token'),
    path('edit/<int:pk>', views.Edit_user.as_view(), name='core_token'),
]