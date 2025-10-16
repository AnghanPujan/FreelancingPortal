from rest_framework import serializers
from .models import Freelancer

class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = '__all__'
        read_only_fields = ('user',)

class FreelancerProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ['profile_picture']