from django.urls import path
from .views import feedback_views

urlpatterns = [
    path('', feedback_views, name="feedback"),
]
