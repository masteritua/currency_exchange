from currency import model_choices as mch
from django.db import models


# Create your models here.

class Rate(models.Model):
	currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
	created = models.DateTimeField(auto_now_add=True)
	buy = models.DecimalField(max_digits=4, decimal_places=2)
	sell = models.DecimalField(max_digits=4, decimal_places=2)
	source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
