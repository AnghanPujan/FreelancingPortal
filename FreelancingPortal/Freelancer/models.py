from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

class Reviews(models.Model):
    enterpriseId = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enterprise_reviews'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    contractId = models.CharField(max_length=100)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Freelancer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    payment_details = models.JSONField(default=dict, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    projects_completed = models.PositiveIntegerField(default=0)
    resume_url = models.URLField(blank=True, null=True)
    certifications = models.JSONField(default=list, blank=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    profile_picture = models.ImageField(upload_to="uploads/freelancer_pics/", blank=True, null=True)
    binanceId = models.CharField(max_length=100, blank=True, null=True, unique=True)
    bio = models.TextField(blank=True, null=True)
    availability = models.BooleanField(default=True)
    social_media_links = models.JSONField(default=dict, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    work_experience = models.JSONField(default=list, blank=True)
    projects = models.JSONField(default=list, blank=True)
    education = models.JSONField(default=list, blank=True)
    reviews = models.ManyToManyField(
        'Reviews',
        related_name='freelancer_reviews',
        blank=True
    )
    achievements = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or str(self.user)