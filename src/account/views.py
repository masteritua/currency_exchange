# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView
from .models import User, Contact
from currency.models import Rate

class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email', )
    success_url = reverse_lazy('home')


class LatestRates(ListView):
    template_name = 'latest_rates.html'
    queryset = Rate.objects.all().order_by('-id')[:20][::1]
    fields = ('currency', 'buy', 'sale', 'source', 'created')


class ContactUs(CreateView):
    template_name = 'my_profile.html'
    queryset = Contact.objects.all()
    fields = ('email', 'title', 'body')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        print(self.object)
        # send_email_async.delay()
        return response


class SignUp(CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'
