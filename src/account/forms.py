from django import forms
from account.models import User, ActivationCodeSMS


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password'] != cleaned_data['password2']:
                raise forms.ValidationError('Passwords do not match!')
        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)  # no save to database

        user.set_password(self.cleaned_data['password'])  # password should be hashed!
        user.is_active = False  # user cannot login
        user.save()

        activation_code = user.activation_codes.create()
        activation_code.send_activation_code()



        # Save code SMS
        random_number = random(6)

        try:

            ac = ActivationCodeSMS.objects.select_related('user')
            ac.is_activated = False
            ac.code = random_number
            ac.save()

        except (RuntimeError, TypeError, NameError):
            raise Exception("Request Error")


        return user


class SignUpFormCodeSMS(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = ActivationCodeSMS
        fields = ('code',)

    def clean(self):

        cleaned_data = super().clean()

        if not self.errors:

            if cleaned_data['code']:

                ac = get_object_or_404(
                    ActivationCodeSMS.objects.select_related('user'),
                    is_activated=False, code=cleaned_data['email'],
                )

                if not ac.code:
                    raise forms.ValidationError('Code do not match!')

            if cleaned_data['email']:
                raise forms.ValidationError('Email do not match!')

        return cleaned_data

    def save(self, commit=True):

        try:

            ac = ActivationCodeSMS.objects.select_related('user')
            ac.is_activated = True
            ac.save(update_fields=['is_activated'])

        except (RuntimeError, TypeError, NameError):
            raise Exception("Request Error")


        return redirect('index')



