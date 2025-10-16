from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Enterprise
from .serializers import EnterpriseSerializer, EnterpriseLogoSerializer

class EnterpriseListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        enterprises = Enterprise.objects.all()
        serializer = EnterpriseSerializer(enterprises, many=True)
        return Response(serializer.data)

    def post(self, request):
        if Enterprise.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Profile already exists for this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = EnterpriseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnterpriseDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, user_id):
        enterprise = get_object_or_404(Enterprise, user=user_id)
        serializer = EnterpriseSerializer(enterprise)
        return Response(serializer.data)

    def put(self, request, user_id):
        enterprise = get_object_or_404(Enterprise, user=user_id)
        if enterprise.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to edit this profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = EnterpriseSerializer(enterprise, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        if not request.user.is_staff:
            return Response(
                {"error": "Only administrators can delete profiles."},
                status=status.HTTP_403_FORBIDDEN
            )
        enterprise = get_object_or_404(Enterprise, pk=user_id)
        enterprise.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EnterpriseLogoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user_id = request.query_params.get('userId')
        if not user_id:
            return Response({"error": "The 'userId' query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(user_id) != request.user.id:
            return Response({"error": "You can only upload to your own profile."}, status=status.HTTP_403_FORBIDDEN)

        profile = get_object_or_404(Enterprise,user=request.user.id)
        serializer = EnterpriseLogoSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)