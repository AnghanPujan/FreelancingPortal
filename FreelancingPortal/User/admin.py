from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'name', 'role')
    list_filter = ('is_active', 'is_staff', 'role', "date_joined")
    ordering = ('date_joined',)