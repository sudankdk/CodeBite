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