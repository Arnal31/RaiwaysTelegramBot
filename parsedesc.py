import requests

from bs4 import BeautifulSoup


def descparse(train):
    train = train.replace('*', '').replace('44', '43').replace('86', '85')
    requ = requests.Session()

    url = f'https://bilet.railways.kz/api/v1/ktj/train/information?name={train}'
    req = requ.get(url)
    if req.status_code == 404:
        return 'Нет описания'
    else:
        text = req.json()['content']
        soup = BeautifulSoup(text, 'lxml')
        desc = soup.get_text()
        return desc

