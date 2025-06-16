from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import register,Login,logout,SkillApi,ProfileApi

router = DefaultRouter()
router.register(r'skills', SkillApi, basename='skills')
router.register(r'profile',ProfileApi,basename="profile")
urlpatterns = [
    path("register/", register),
    path("login/", Login.as_view()),
    path("logout/", logout),
    path("", include(router.urls)), 
]

