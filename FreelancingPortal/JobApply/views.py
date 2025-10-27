from django.shortcuts import render
from .models import JobApplication
from .serializers import JobApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permission import IsFreelancer
from rest_framework import status


# create your views here.
class JobApplicationCreateView(APIView):
    permission_classes = [IsFreelancer, IsAuthenticated]

    def post(self, request):
        if JobApplication.objects.filter(job_id=request.data.get('job'), freelancer=request.user.freelancer).exists():
            return Response({"detail": "You have already applied for this job. Update It!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Not applied yet")
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            print(request.user.freelancer)
            serializer.save(freelancer=request.user.freelancer)
            print("Saved successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)