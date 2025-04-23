from rest_framework import viewsets
from .models import User, SOSRequest
from .serializers import UserSerializer, SOSRequestSerializer
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SOSRequestViewSet(viewsets.ModelViewSet):
    queryset = SOSRequest.objects.all()
    serializer_class = SOSRequestSerializer
    permission_classes = [IsAuthenticated]
