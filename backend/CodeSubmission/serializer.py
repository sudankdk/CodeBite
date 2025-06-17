from rest_framework import serializers
from .models import CodeSubmission,Bid,Session,Review
from profile.serializers import MyUserSerializer,SkillsSerializer

class CodeSubmissionSerializer(serializers.ModelSerializer):
    user= MyUserSerializer(read_only=True)
    skill= SkillsSerializer(read_only=True,many=True)
    class Meta:
        model= CodeSubmission
        fields=["id",'user','skill','content_type','session_type','accepted_bid','status','code','video_url','gist_url']
        
class BidSerializer(serializers.ModelSerializer):
    reviewer= MyUserSerializer(read_only=True)
    submission=CodeSubmissionSerializer(read_only=True)
    
    class Meta:
        model= Bid
        fields=['id','reviewer','submission','price','availability','status']