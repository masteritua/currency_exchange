from django.shortcuts import render
from .models import FeedbackModel
from django.views.generic import CreateView


class FeedbackCreateView(CreateView):
  model = FeedbackModel
  fields = ('title', 'description')

  success_url = "/"


def feedback_views(request):
  if request.method == 'POST':

    form = FeedbackModel(request.POST)
    if form.is_valid():
      feedback_task.delay(form)

      return HttpResponseRedirect(reverse('feedback'))

  else:
    form = FeedbackModel(initial=post)

  return render(request, 'feedback.html', context={"form": form})
