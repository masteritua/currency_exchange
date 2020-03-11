from django.db import models


# Create your models here.
class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=256)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
