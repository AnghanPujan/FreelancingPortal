from .models import JobApplication
from rest_framework import serializers

class JobApplicationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['freelancer', 'status', 'created_at', 'updated_at']