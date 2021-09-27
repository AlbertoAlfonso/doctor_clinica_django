from django.urls import path
from django.urls.conf import include
from petition import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.PetitionViewSet, basename='petitions')
router.register('find_by_patient', views.PetitionViewSet, basename='find_by_patient')
router.register('find_by_doctor', views.PetitionViewSet, basename='find_by_doctor')
router.register('answer', views.PetitionViewSet, basename='answer')

app_name = 'petition'
urlpatterns = [
    path('find_by_user/', views.FindPetitionUser.as_view() , name='find_user'),
    path('', include(router.urls))

#    router.post('/save', petitionController.createPetition);
#    router.post('/date/test', petitionController.date);
#    router.post('/edit/:id', petitionController.editPetition);
#    router.get('/find/:id', petitionController.index)
#    router.get('/find/doctor/:id,:page', petitionController.findPetitionbyDoctor);
#    router.get('/find/patient/:id,:page', petitionController.findPetitionbyPatient)
#    router.get('/delete/:id', petitionController.deletebyId)
#    router.post('/answer/:id', petitionController.answerbyId)
]