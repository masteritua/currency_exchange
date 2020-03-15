from django.urls import path
from .views import FeedbackCreateView

urlpatterns = [
    path('create', FeedbackCreateView.as_view(), name='feedback_create')
]
