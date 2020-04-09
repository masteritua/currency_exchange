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

        activation_code_sms = user.activation_codes_sms.create()
        activation_code_sms.send_activation_code_sms()

        return user


class SignUpFormCodeSMS(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = ActivationCodeSMS
        fields = ('code', 'email')


    def clean(self):

        cleaned_data = super().clean()

        if not self.errors:

            user = User.objects.filter(email=cleaned_data['email']).last()

            if not user:
                raise forms.ValidationError('Такого email не существует!')

            sms = ActivationCodeSMS.objects.filter(user=user.id, code=cleaned_data['code'], is_activated=False).last()

            if not sms:
                raise forms.ValidationError('Код неверный или уже активирован!')

        return cleaned_data

    def save(self, commit=True):

        cleaned_data = super().clean()

        user = User.objects.filter(email=cleaned_data['email']).last()
        user.is_active = True
        user.save(update_fields=['is_active'])

        sms = ActivationCodeSMS.objects.filter(user=user.id, code=cleaned_data['code']).last()
        sms.is_activated = True
        sms.save(update_fields=['is_activated'])

        return sms

