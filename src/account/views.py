# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView, View
from .models import User, Contact, ActivationCode
from currency.models import Rate
from account.forms import SignUpForm, SignUpFormCodeSMS

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


class SignUpView(CreateView):
    template_name = 'signup.html'
    queryset = User.objects.all()
    success_url = reverse_lazy('home')
    form_class = SignUpForm


class SignUpCodeSMSView(CreateView):
    template_name = 'signupcodesms.html'
    queryset = User.objects.all()
    success_url = reverse_lazy('home')
    form_class = SignUpFormCodeSMS


class Activate(View):
    def get(self, request, activation_code):
        ac = get_object_or_404(
            ActivationCode.objects.select_related('user'),
            code=activation_code, is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('home')