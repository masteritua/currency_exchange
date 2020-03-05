CURR_USD, CURR_EUR = range(1, 3)

CURRENCY_CHOICES = (
	(CURR_USD, 'USD'),
	(CURR_EUR, 'EUR'),
)

SR_PRIVAT, SR_MONO, SR_OSHADBANK, SR_ALFA, SR_AVAL = range(1, 6)

SOURCE_CHOICES = (
	(SR_PRIVAT, 'PrivatBank'),
	(SR_MONO, 'MonoBank'),
	(SR_OSHADBANK, 'Ощадбанк'),
	(SR_ALFA, 'Альфа-банк'),
	(SR_AVAL, 'Аваль'),
)

ISO_STANDART = (
	(840, 'USD'),
	(978, 'EUR'),
	(980, 'UAH'),
)
