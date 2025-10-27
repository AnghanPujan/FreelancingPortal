from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

class Reviews(models.Model):
    freelancerId = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='freelancer_reviews'
    )
    rating = models.PositiveIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)]
)
    contractId = models.CharField(max_length=100)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Enterprise(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='enterprise_profile'
    )
    company_name = models.CharField(max_length=255, blank=True, null=True)
    industry_type = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="uploads/enterprise_logos/", blank=True, null=True)
    contactPerson = models.JSONField(default=dict, blank=True)
    location = models.JSONField(max_length=255, blank=True, null=True)
    preferred_currency = models.CharField(max_length=10, blank=True, null=True)
    preferred_payment_method = models.CharField(max_length=50, blank=True, null=True)
    vat_or_gst_id = models.CharField(max_length=50, blank=True, null=True)
    social_media_profile = models.URLField(blank=True, null=True)
    binanceId = models.CharField(max_length=100, blank=True, null=True)
    reviews = models.ManyToManyField(
        'Reviews',
        related_name='enterprise_reviews',
        blank=True
    )
    previous_projects = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        result = self.reviews.aggregate(average=Avg('rating'))
        avg = result.get('average')
        return round(avg, 1) if avg is not None else 0

    def __str__(self):
        return self.company_name or str(self.user)