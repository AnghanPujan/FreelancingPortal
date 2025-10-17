from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8
    )
    cnf_password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'password', 'cnf_password')
        extra_kwargs = {
            'name': {'required': True},
            'role': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['cnf_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('cnf_password')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user
    
    def create_superuser(self, validated_data):
        validated_data.pop('cnf_password')
        
        user = User.objects.create_superuser(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            role=validated_data.get('role', 'admin'),
            is_staff=True,
            is_superuser=True,
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email
        token['role'] = user.role
        user = User.objects.filter(email=user.email)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            'id': self.user.id,
            'name': self.user.name,
            'email': self.user.email,
            'role': self.user.role,
        }
        return data

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    
    def validate(self, attrs):
        print("Iside validate fiunction")
        token_str = attrs.get('refresh_token')
        if not token_str or not isinstance(token_str, str):
            print("Exception Raised")
            raise serializers.ValidationError("A valid refresh token is required.")
        return attrs