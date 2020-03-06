from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import ContactModel
from django.views.generic import CreateView
from currency.tasks import feedback_task
from django.urls import reverse_lazy


class FeedbackCreateView(CreateView):
    template_name = 'feedback_form.html'
    queryset = ContactModel.objects.all()
    fields = ('email', 'title', 'text')
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        response = super().form_valid(form)
        feedback_task.delay(self.object.all())
        return response
