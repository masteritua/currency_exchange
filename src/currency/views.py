from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
# Create your views here.
def test(self):

	url = 'https://www.oschadbank.ua/ua/private/currency'
	page = requests.get(url)

	soup = BeautifulSoup(page.content)
	film_list = soup.find('table', {'class': 'table'})
	items = film_list.find_all('tr')
	for item in items:
		i = item.find_all('td')

		if bool(i) is True:

			print(i)

			breakpoint()

	return HttpResponse("Тестовая запись")
