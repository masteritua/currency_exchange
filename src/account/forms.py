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

        ac = get_object_or_404(
            ActivationCodeSMS.objects.select_related('user'),
            is_activated=False,
        )

        ac.save(code=random_number)


        # Send code to SMS
        ActivationCodeSMS.send_activation_code(random_number)


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
                    is_activated=False,code=cleaned_data['email'],
                )

                if not ac.code:
                    raise forms.ValidationError('Code do not match!')

            if cleaned_data['email']:
                raise forms.ValidationError('Email do not match!')

        return cleaned_data

    def save(self, commit=True):

        ac = get_object_or_404(
            ActivationCodeSMS.objects.select_related('user'),
            is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')

        return redirect('index')



