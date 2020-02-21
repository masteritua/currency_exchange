CURR_USD, CURR_EUR = range(1, 3)

CURRENCY_CHOICES = (
	(CURR_USD, 'USD'),
	(CURR_EUR, 'EUR'),
)

SR_PRIVAT, SR_MONO = range(1, 3)
SOURCE_CHOICES = (
	(SR_PRIVAT, 'PrivatBank'),
	(SR_MONO, 'MonoBank'),
)

ISO_STANDART = (
	(840, 'USD'),
	(978, 'EUR'),
	(980, 'UAH'),
)
