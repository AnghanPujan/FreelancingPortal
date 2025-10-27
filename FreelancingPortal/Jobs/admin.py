from django.contrib import admin
from .models import Job

# Register your models here.
@admin.register(Job)
class jobs(admin.ModelAdmin):
    list_display = ('title', 'enterprise', "is_visible", "created_at", "updated_at")
    search_fields = ('title', 'enterprise')