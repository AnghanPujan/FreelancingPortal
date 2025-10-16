from django.db import models
from Freelancer.models import Freelancer

class Review(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, help_text="Rating between 0 and 5")
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.freelancer} - {self.rating}/5"
