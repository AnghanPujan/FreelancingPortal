from django.urls import path
from .views import (
    EnterpriseListCreateView,
    EnterpriseDetailView,
    EnterpriseLogoUploadView,
)

urlpatterns = [
    path('', EnterpriseListCreateView.as_view(), name='enterprise-list-create'),
    path('upload/profile-picture/', EnterpriseLogoUploadView.as_view(), name='enterprise-upload-logo'),
    path('<int:user_id>/', EnterpriseDetailView.as_view(), name='enterprise-detail'),
]