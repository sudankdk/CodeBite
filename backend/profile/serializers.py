from rest_framework import serializers
from .models import MyUser,Skills,Profile
from django.contrib.auth.hashers import make_password


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields="__all__"

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=MyUser
        fields=("username","email","password")
        
    def create(self, validated_data):
            validated_data['password']=make_password(validated_data['password'])
            return super().create(validated_data)

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Skills
        fields="__all__"
        
class ProfileSerializer(serializers.ModelSerializer):
    user= MyUserSerializer(read_only=True)
    skills_offered= SkillsSerializer(many=True,read_only=True)
    skills_sought= SkillsSerializer(many=True, read_only=True)
    
    class Meta:
        model= Profile
        fields=['id',
            'user',
            'bio',
            'skills_offered',
            'skills_sought',
            'average_rating',
            'review_count',
            'profile_image',
            'location',
            'created_at',
            'updated_at']