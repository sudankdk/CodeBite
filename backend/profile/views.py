from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import RegisterSerializer,MyUserSerializer,SkillsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from .models import Skills
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication





@api_view(['POST'])
def register(request):
    user= RegisterSerializer(data=request.data)
    if user.is_valid():
        user.save(
        )
        return Response(user.data)
    return Response({"error": "Registration failed!! Try again", "details": user.errors})


class Login(TokenObtainPairView):
    def post(self,request,*args,**kwargs):
        response = super().post(request,*args,**kwargs)
        refresh= response.data['refresh']
        access= response.data['access']
        
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=3600,
        )
        
        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=7*24*3600,
        )
        return response

class Refresh(TokenRefreshView):
    def post(self,request,*args,**kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh']=refresh_token
            response= super().post(request,*args,*kwargs)
            access_token = response.data['access']
            
            response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=3600,
            )
            return Response({"message": "Refreshed successful"})
            
        except Exception as e:
            return Response({
                "error": e
            })

@api_view(['POST'])
def logout(request):
    response = Response({"message": "Logged out"})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

class SkillApi(ModelViewSet):
    serializer_class=SkillsSerializer
    queryset=Skills.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    