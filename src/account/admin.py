from django.contrib import admin
import os.path
from account.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.settings import BASE_DIR

@receiver(pre_save, sender=User)
def pre_profile(sender, instance, **kwargs):

    path = f'{BASE_DIR}/media/avatar/'
    for file in os.scandir(path):
        os.unlink(file.path)


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'username', 'is_active', 'avatar']

admin.site.register(User, UserAdmin)