celery -A main worker -l info
celery -A main beat -l info -S django