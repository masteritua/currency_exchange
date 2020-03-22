import random
from time import sleep
from ./../src/account.models import WorkUaDetails

def save_db(list):
    w =  WorkUaDetails(list)
    w.save()


def save_json(list):

    with open('json.txt', 'a') as file:
        file.write(' | '.join(list) + '\n')


def save_info(array: list) -> None:
    with open('workua2.txt', 'a') as file:
        for line in array:
            file.write(' | '.join(line) + '\n')

def random_sleep():
    sleep(random.randint(1, 4))
