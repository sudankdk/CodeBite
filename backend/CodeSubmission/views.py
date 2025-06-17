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
    
    @action(detail=True,methods=['post'])
    def accept_bid(self,request,pk=None):
        codesubmission=self.get_object()
        bid_id=request.data.get("bid")
        if not bid_id:
                return Response({"error": "Bid ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            bid=Bid.objects.get(id=bid_id,submission=codesubmission)
            pass
        except Bid.DoesNotExist:
                 return Response({"error": "Invalid bid ID for this submission."}, status=status.HTTP_404_NOT_FOUND)


        codesubmission.accepted_bid=bid
        codesubmission.status="locked"
        codesubmission.save()
        serializer=self.get_serializer(codesubmission)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class BidApi(ModelViewSet):
    queryset= Bid.objects.all()
    serializer_class=BidSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    