from django.urls import path, include
from . views import (
    FreelancerJobApplicationsView,
    JobApplicationCreateView,
    ) 
# upload cover letter file -- upload/coverletter?userId=userId&uploadType=coverletter&role=freelancer
# apply job -- /api/jobApply/ -- POST
# update application status -- http://localhost:5001/api/jobApply/:id
# get freelancer applications for job -- http://localhost:5001/api/jobApply/applications/:jobId?search=react&availability=true&minRating=3
# get all jobs applied by freelancer -- http://localhost:5001/api/jobApply/application/freelancers/:freelancerId
# get application for job by freelancer -- http://localhost:5001/api/jobApply/application/:jobId/:freelancerId

urlpatterns = [
    path('', JobApplicationCreateView.as_view(), name='job-application-create'),
]

