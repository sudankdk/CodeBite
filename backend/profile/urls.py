from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import register,Login,logout,SkillApi

router = DefaultRouter()
router.register(r'skills', SkillApi, basename='skills')
urlpatterns = [
    path("register/", register),
    path("login/", Login.as_view()),
    path("logout/", logout),
    path("", include(router.urls)),  # include all router-generated URLs here
]

