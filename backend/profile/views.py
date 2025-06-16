from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import RegisterSerializer,MyUserSerializer,SkillsSerializer,ProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from .models import Skills,Profile
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action






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
    
    
class ProfileApi(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset=Profile.objects.all()
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    
    @action(detail=False,methods=['get'])
    def me(self,request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer=self.get_serializer(profile)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['post'])
    def add_skill_sought(self,request):
        try:
            profile=Profile.objects.get(user=request.user)
            skill_id= request.data.get('skills',[])
            if not isinstance(skill_id,list):
                return Response({
                    "error":"Expected a list of id",

                },status=status.HTTP_400_BAD_REQUEST)
            skills=Skills.objects.filter(id__in=skill_id)
            profile.skills_sought.add(*skills)
            profile.save()
            serializer= self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Error in adding skills: {e}"
            })
    
    @action(detail=False, methods=['post'])
    def add_skill_offered(self,request):
        try:
            profile=Profile.objects.get(user=request.user)
            skill_id= request.data.get('skills',[])
            if not isinstance(skill_id,list):
                return Response({
                    "error":"Expected a list of id",

                },status=status.HTTP_400_BAD_REQUEST)
            skills=Skills.objects.filter(id__in=skill_id)
            profile.skills_offered.add(*skills)
            profile.save()
            serializer= self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Error in adding skills: {e}"
            })
            
    @action(detail=True, methods=['post'])
    def rate_user(self,request,pk=None):
        try:
            profile= self.get_object()
            rating = request.data.get("rating")
            if rating is None:
                return Response({"error": "rating must be a number and cannot be none."},status=status.HTTP_400_BAD_REQUEST)
            
            try:
                rating = float(rating)
                if rating < 0 or rating > 5:
                    return Response({"error": "Rating must be between 0 and 5."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Invalid rating format."}, status=status.HTTP_400_BAD_REQUEST)
            profile.update_rating(rating)
            serializer= self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error":f"Error in rating users: {e}"
            })