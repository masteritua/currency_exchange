from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import ContactModel
from django.views.generic import CreateView
from currency.tasks import feedback_task
from django.urls import reverse


class FeedbackCreateView(CreateView):
    model = ContactModel
    fields = ('email', 'title', 'text')

    success_url = "/"


def feedback_views(request):
    if request.method == 'POST':

        form = ContactModel(request.POST)
        if form.is_valid():
            form.save();
            feedback_task.delay(request.POST)

            return HttpResponseRedirect(reverse('feedback'))

    else:
        form = ContactModel(initial=request.POST)

    return render(request, 'feedback.html', context={"form": form})
