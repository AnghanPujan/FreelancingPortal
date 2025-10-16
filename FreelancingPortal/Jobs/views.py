from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Job
from .serializers import JobSerializer
from Enterprise.models import Enterprise

class JobListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        jobs = Job.objects.filter(is_visible=True)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            enterprise_profile = request.user.enterprise_profile
        except Enterprise.DoesNotExist:
            return Response(
                {"error": "Only enterprise users can post jobs."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(enterprise=enterprise_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        if job.enterprise.user != request.user:
            return Response(
                {"error": "You do not have permission to edit this job."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        
        if job.enterprise.user != request.user:
            return Response(
                {"error": "You do not have permission to delete this job."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EnterpriseJobListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, enterprise_id):
        jobs = Job.objects.filter(enterprise__user_id=enterprise_id, is_visible=True)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
class EnterpriseJobListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, enterprise_id):
        jobs = Job.objects.filter(enterprise__user_id=enterprise_id, is_visible=True)
        serializer = JobSerializer(jobs, many=True)
        
        return Response(serializer.data)