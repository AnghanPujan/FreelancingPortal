from django.urls import path
from .views import FreelancerView, FreelancerProfileView, FreelancerProfilePictureUploadView

urlpatterns = [
    # All the freelancer
    path('', FreelancerView.as_view(), name='freelancer-list'),
    # Freelancer profile by id
    path('<int:user_id>/', FreelancerView.as_view(), name='freelancer-detail'),
    # Freelancer's own profile
    path('profile/', FreelancerProfileView.as_view(), name='freelancer-self-profile'),
    # Upload profile picture
    path('upload/profile-picture/', FreelancerProfilePictureUploadView.as_view(), name='freelancer-upload-picture'),
]