from currency.tasks import feedback_task
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Contact


class FeedbackCreateView(CreateView):
  template_name = 'feedback_form.html'
  queryset = Contact.objects.all()
  fields = ('email', 'title', 'text')
  success_url = reverse_lazy('home')

  def form_valid(self, form):
    response = super(FeedbackCreateView, self).form_valid(form)
    feedback_task.delay(self.object)
    return response
