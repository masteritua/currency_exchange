from currency import model_choices as mch
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from currency.tasks import send_message


class Rate(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
	buy = models.DecimalField(max_digits=4, decimal_places=2)
	sale = models.DecimalField(max_digits=4, decimal_places=2)
	source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)

	def __str__(self):
		return f'{self.created} {self.get_currency_display()} {self.buy} {self.sale}'


@receiver(post_save, sender=Rate)
def save_profile(sender, instance, **kwargs):
	send_message.delay("Отчет", "Создание новой записи Rate")