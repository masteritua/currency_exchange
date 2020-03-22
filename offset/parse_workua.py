from user_agent import generate_user_agent
from utils import random_sleep, save_info, save_db,save_json

import requests
from bs4 import BeautifulSoup

# global variables
HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'

def page_into(href, headers):

    response = requests.get(HOST + href, params={}, headers=headers)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find('div', class_="card wordwrap")
    data={}

    for el_p in container.find_all('p'):


        if el_p.select('span[title="Зарплата"]'):
            data['celery'] = el_p.b.text

        if el_p.select('span[title="Данные о компании"]'):
            data['company']=el_p.b.text

        if el_p.select('span[title="Адрес работы"]'):
            data['address']=el_p.text

        if el_p.select('span[title="Условия и требования"]'):
            data['rules']=el_p.text

    data['descriptin']=soup.select('div[id="job-description"]')

    return data


def main():
    page = 0

    data_json ={}
    while True:
        page += 1

        payload = {
           'ss': 1,
           'page': page,
        }
        user_agent = generate_user_agent()
        headers = {
            'User-Agent': user_agent,
        }

        print(f'PAGE: {page}')
        response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
        response.raise_for_status()
        # random_sleep()

        # if response.status_code != 200:
        #     print('something wrong!')
        #     break

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        class_ = 'card card-hover card-visited wordwrap job-link'
        cards = soup.find_all('div', class_=class_)
        if not cards:
            cards = soup.find_all('div', class_=class_ + ' js-hot-block')

        result = []
        if not cards:
            # from pdb import set_trace
            # set_trace()
            break

        for card in cards:
            tag_a = card.find('h2').find('a')
            title = tag_a.text
            href = tag_a['href']

            # Парсинг внутренней страницы
            page_into_var=page_into(href, headers)
            save_db(page_into_var)
            data_json.append(page_into_var)

            result.append([title, href])
            # get vacancy full info

        save_info(result)

    save_json(data_json)

if __name__ == "__main__":
    main()

# 1 parse vacancy details - 6
# 2 save all info to sqlite database (CREATE TABLE, INSERT VALUES INTO TABLE) - 2
# 3 save to json file! vacancy.json [{}, {}, {}] - 2
