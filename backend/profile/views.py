from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import RegisterSerializer,MyUserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def register(request):
    user= RegisterSerializer(data=request.data)
    if user.is_valid():
        user.save(
        )
        return Response(user.data)
    return Response({"error":" Registration failed!! Try again"})


class Login(TokenObtainPairView):
    def post(self,request,*args,**kwargs):
        response = super().post(request,*args,**kwargs)
        refresh= response.data['refresh']
        access= response.data['access']
        
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=3600,
        )
        
        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=7*24*3600,
        )
        return response
