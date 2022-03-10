from bs4 import BeautifulSoup
import requests
import re


async def get_html_doc(ref):
    """
    Получает HTML документ в виде текста.
    :return: Возвращает объект BeautifulSoup с полученным HTML.
    """
    html_doc = requests.get(ref).text
    soup = BeautifulSoup(html_doc, 'lxml')
    return soup


def find_link_and_name(html_doc):
    """
    Ищет в HTML документе название блюда и его рецепт.
    :return: Возвращает кортеж (название_блюда, ссылка)
    """

    receipt_link = html_doc.find('a', class_='btnGreen2 flR', attrs={
                         'target': '_new'
                     })
    receipt_name = html_doc.find('h1')

    pattern_link = r'www.gotovim.ru/sbs/\D+.shtml'
    pattern_name = r'\w+'
    return ' '.join(re.findall(pattern_name, str(receipt_name))[1:-1]), \
           r'http://' + re.findall(pattern_link, str(receipt_link))[0]


def parse_receipt(html_doc):
    """
    Парсит страницу рецепта и получает из него текст.
    :return: Возвращает словарь - {
                            name: название_рецепта,
                            ingridients: [
                                (название_ингридиента, количество),
                                ...
                                ],
                            receipt_text: [шаг1: srt, шаг2: str, ..., шагN]
                            }
    """
    receipt_name = html_doc.find('h1').contents[0]

    ingridients_li = html_doc.find_all('li', attrs={
                                        'itemprop': 'recipeIngredient'})
    ingridients = (i.contents[0] for i in ingridients_li)

    receipt_text_p = html_doc.find_all('p', attrs={
                                            'itemprop': 'recipeInstructions'})
    receipt_text = (i.contents for i in receipt_text_p)
    receipt_res = []
    for i in receipt_text:
        receipt_res += i

    return {
        'name': receipt_name,
        'ingridients': (i for i in ingridients),
        'receipt_text': (i.strip() for i in receipt_res),
    }



if __name__ == '__main__':
    pass
