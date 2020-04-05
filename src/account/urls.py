# accounts/urls.py
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('profile/<int:pk>/', views.MyProfile.as_view(), name='my-profile'),
    path('contact-us/', views.ContactUs.as_view(), name='contact-us'),
    path('latest-rates/', views.LatestRates.as_view(), name='latest-rates'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uuid:activation_code>/', views.Activate.as_view(), name='activate'),
    path('signup-activate-sms/', views.SignUpCodeSMSView.as_view(), name='signup-activate-sms'),

    path('about/', views.About.as_view(), name='about'),
    path('experience/', views.Experience.as_view(), name='experience'),
    path('education/', views.Education.as_view(), name='education'),
    path('skills/', views.Skills.as_view(), name='skills'),
    path('interests/', views.Interests.as_view(), name='interests'),
]
