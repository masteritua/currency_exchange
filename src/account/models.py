from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from currency.tasks import send_message
from account.tasks import send_activation_code_async

def avatar_path(instance, filename):
    m = 1
    return "/".join(["avatar", str(instance.id), str(uuid4()), filename])

class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True, default=None)


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=256)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} {self.title} {self.body} {self.created}'



class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes')
    created = models.DateTimeField(auto_now_add=True)
    # code = models.CharField(max_length=128)
    code = models.UUIDField(default=uuid4, editable=False, unique=True)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    def send_activation_code(self):
        send_activation_code_async.delay(self.user.email, self.code)

    # def save(self, *args, **kwargs):
    #     self.code = ... # GENERTE CODE
    #     super().save(*args, **kwargs)


class ActivationCodeSMS(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes_sms')
    created = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        send_activation_code_async_sms.delay(self.user.email, self.user.code)

@receiver(post_save, sender=Contact)
def save_profile(sender, instance, **kwargs):
	send_message.delay("Отчет", "Создание новой записи таблице Соntact")
