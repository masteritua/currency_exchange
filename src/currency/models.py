from currency import model_choices as mch, tasks as t
from django.db.models import DateTimeField, PositiveSmallIntegerField, DecimalField,Model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Rate(Model):
	created = DateTimeField(auto_now_add=True)
	currency = PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
	buy = DecimalField(max_digits=4, decimal_places=2)
	sale = DecimalField(max_digits=4, decimal_places=2)
	source = PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)

	def __str__(self):
		return f'{self.created} {self.get_currency_display()} {self.buy} {self.sale}'


@receiver(post_save, sender=Rate)
def save_profile(sender, instance, **kwargs):
	t.send_message.delay("Отчет", "Создание новой записи Rate")