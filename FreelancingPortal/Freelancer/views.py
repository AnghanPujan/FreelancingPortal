from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Freelancer
from .serializers import FreelancerSerializer, FreelancerProfilePictureSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class FreelancerView(APIView):
    def get_permissions(self):
        if str(self.request.method).upper == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request, user_id=None):
        if user_id:
            profile = get_object_or_404(Freelancer, pk=user_id)
            serializer = FreelancerSerializer(profile)
            return Response(serializer.data)
        else:
            freelancers = Freelancer.objects.all()
            serializer = FreelancerSerializer(freelancers, many=True)
            return Response(serializer.data)

    def delete(self, request, user_id):
        profile = get_object_or_404(Freelancer, pk=user_id)
        profile.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FreelancerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = Freelancer.objects.get_or_create(user=request.user)
        serializer = FreelancerSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        if Freelancer.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Profile already exists. Use PUT to update."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = FreelancerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        profile, created = Freelancer.objects.get_or_create(user=request.user)
        serializer = FreelancerSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FreelancerProfilePictureUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request):
        user_id= request.query_params.get('userId')

        if not user_id:
            return Response(
                {"error": "The 'userId' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if int(user_id) != request.user.id:
            return Response(
                {"error": "You can only update your own profile picture."},
                status=status.HTTP_403_FORBIDDEN
            )

        profile = get_object_or_404(Freelancer, pk=request.user.id)
        serializer = FreelancerProfilePictureSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)