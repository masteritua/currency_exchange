# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from feedback.views import FeedbackCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),  # new
    path('account/', include('django.contrib.auth.urls')),
    path('currency/', include('currency.urls')),
    path('feedback/', include('feedback.urls')),
    url('feedbacknew/', FeedbackCreateView.as_view(), name='feedback_new'),
    path('', TemplateView.as_view(template_name='home.html'), name='home')
]
