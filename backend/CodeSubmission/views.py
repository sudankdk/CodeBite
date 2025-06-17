from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from profile.models import MyUser
from .models import CodeSubmission,Bid
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import CodeSubmissionSerializer,BidSerializer


class CodeSubmissionApi(ModelViewSet):
    queryset = CodeSubmission.objects.all()
    serializer_class = CodeSubmissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['get'])
    def my_submissions(self,request):
        submissions= CodeSubmission.objects.filter(user=request.user)
        serializer= self.get_serializer(submissions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class BidApi(ModelViewSet):
    queryset= Bid.objects.all()
    serializer_class=BidSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    