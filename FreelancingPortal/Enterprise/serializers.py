from rest_framework import serializers
from .models import Enterprise

class EnterpriseSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Enterprise
        fields = '__all__'
        read_only_fields = ('user',)

class EnterpriseLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ['logo']