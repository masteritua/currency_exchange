from django.urls import path
from .views import feedback_views
from feedback.views import FeedbackCreateView

urlpatterns = [
    path('', feedback_views, name="feedback"),
    path('feedback-create', FeedbackCreateView.as_view(), name='feedback_create')
]
