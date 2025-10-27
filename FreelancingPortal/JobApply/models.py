from django.db import models

class JobApplication(models.Model):
    STATUS_CHOICES = [
        (1, 'Applied'),
        (2, 'Under Review'),
        (3, 'Accepted'),
        (4, 'Rejected'),
    ]
    ApplicationId = models.AutoField(primary_key=True)

    job = models.ForeignKey(
        'Jobs.Job', 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    freelancer = models.ForeignKey(
        'Freelancer.Freelancer', 
        on_delete=models.CASCADE, 
        related_name='job_applications'
    )
    enterprise = models.ForeignKey(
        'Enterprise.Enterprise', 
        on_delete=models.CASCADE, 
        related_name='applications_received'
    )
    coverLetterText = models.TextField(blank=True, null=True)
    coverLetterFileUrl = models.URLField(max_length=500, blank=True, null=True)

    proposedBudget = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application for {self.job.title} - Status: {self.get_status_display()}"    