from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    EnterpriseJobListView,
)

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('profile/<int:enterprise_id>/', EnterpriseJobListView.as_view(), name='enterprise-job-list'),
]