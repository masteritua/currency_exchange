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
]
