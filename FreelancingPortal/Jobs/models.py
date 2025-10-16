from django.db import models

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    PRICING_TYPE_CHOICES = [
        ('dailyRate', 'Daily Rate'),
        ('fixedPrice', 'Fixed Price'),
    ]
    DURATION_UNIT_CHOICES = [
        (1, 'Days'),
        (2, 'Weeks'),
        (3, 'Months'),
    ]

    enterprise = models.ForeignKey('Enterprise.Enterprise', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    required_skills = models.JSONField(default=list, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pricing_details = models.CharField(
        max_length=20,
        choices=PRICING_TYPE_CHOICES,
        default='dailyRate'
    )
    duration_unit = models.IntegerField(choices=DURATION_UNIT_CHOICES)
    duration_value = models.IntegerField()
    other_requirements = models.JSONField(default=list, blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title