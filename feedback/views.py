from django.shortcuts import render
from django.views.generic import CreateView
from .models import Campaign


class Email(CreateView):
  model = Email
  fields = ('email', 'title', 'text')

  success_url = "/feedback/list"