from django.contrib import admin
import os.path
from account.models import User
from django.db.models.signals import pre_save

@receiver(pre_save, sender=User)
def pre_profile(sender, instance, **kwargs):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    path = f'{PROJECT_ROOT}/media/avatar/'
    for file in os.scandir(path):
        os.unlink(file.path)


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'username', 'is_active', 'avatar']

admin.site.register(User, UserAdmin)