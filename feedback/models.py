from django.db import models


# Create your models here.
class ContactModel(models.Model):
    email = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
