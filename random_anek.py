import requests
from bs4 import BeautifulSoup

URL = 'https://baneks.ru/random'


def cleaner_p(p):
    p = p.replace('<p>', '')
    p = p.replace('</p>', '')
    p = p.replace('<br/>', '')
    return p


def get_random_joke():
    global URL
    html_doc = requests.get(URL).text
    soup = BeautifulSoup(html_doc,'lxml')
    joke = soup.find('p')
    return cleaner_p(str(joke))


async def send_random_joke(chat_id, text):
    joke = get_random_joke()




if __name__ == '__main__':
    print(get_random_joke())