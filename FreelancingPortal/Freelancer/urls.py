from django.urls import path
from .views import FreelancerView, FreelancerProfileView, FreelancerProfilePictureUploadView

urlpatterns = [
    path('', FreelancerView.as_view(), name='freelancer-list'),
    path('<int:user_id>/', FreelancerView.as_view(), name='freelancer-detail'),
    path('profile/', FreelancerProfileView.as_view(), name='freelancer-self-profile'),
    path('upload/profile-picture/', FreelancerProfilePictureUploadView.as_view(), name='freelancer-upload-picture'),
]