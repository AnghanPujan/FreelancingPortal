from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    enterprise = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'