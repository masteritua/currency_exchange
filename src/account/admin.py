from django.contrib import admin
import os.path
from account.models import User


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'username', 'is_active', 'avatar']

    def after_saving_model_and_related_inlines(self, obj):

        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        path =  f'{PROJECT_ROOT}/media/avatar/{obj.get("avatar")}'
        if os.path.isfile(path):
            os.remove(path)

        return obj

admin.site.register(User, UserAdmin)