from django.urls import path
from django.urls.conf import include
from doctor import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.DoctorViewSet, basename='register')
router.register('page', views.DoctorViewSet, basename='pagination')
# router.register('edit/<int:pk>', views.EditDoctorDetail, basename='login')    ok
# router.register('file', views.DoctorFile, basename='file')
# router.register('state_on/<int:pk>', views.State_on, basename='state_on')
# router.register('state_off/<int:pk>', views.State_off, basename='state_off')
# router.register('get_image', views.ResponseImage, basename='image')
# router.register('doctors/<int:pk>', views.FindAll, basename='state_on')  # pk = pagination
router.register('find_by_speciality/<int:pk>', views.DoctorViewSet, basename='state_on')  # pk = pagination

app_name = 'doctor'
urlpatterns = [
    path('create', views.CreateDoctorView.as_view(), name='create'),
    path('login', views.LoginDoctor.as_view(), name='token'),
    path('edit/<int:pk>/', views.EditDoctorDetail.as_view(), name='edit'),
    path('state/<int:pk>/', views.StateDoctor.as_view(), name='state'),
    path('edit_all/<int:pk>/', views.EditDoctor.as_view(), name='edit2'),
    path('image/<int:pk>/', views.ResponseImage.as_view(), name='image'),
    # path('me', views.ManageDoctorView.as_view(), name='me'),
    path('', include(router.urls))
]