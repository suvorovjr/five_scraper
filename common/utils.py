import random
from uuid import uuid4


def get_headers(shop_id: str) -> dict:
    device_id = str(uuid4()).upper()
    ios_version = f'iOS {random.randint(14, 16)}.{random.randint(1, 7)}.{random.randint(1, 7)}'
    user_agent = f'Browser/3.0.2 (ru.5ka.browser.app; build:5; {ios_version}) Alamofire/5.9.1'
    headers = {
        'accept': 'application/json',
        'accept-language': 'ru-RU;q=1.0',
        'connection': 'keep-alive',
        'host': '5d.5ka.ru',
        'user-agent': user_agent,
        'x-app-version': '3.0.2',
        'x-can-receive-push': 'true',
        'x-device-id': device_id,
        'x-package-name': 'ru.5ka.browser.app',
        'x-platform': 'ios',
        'x-sdk-version': '3.0.2',
        'x-user-store': shop_id,
    }
    return headers


def get_category_params() -> dict:
    params = {
        'include_restrict': 'true',
        'include_subcategories': '1',
        'mode': 'store',
    }
    return params


def get_products_params(products_count: int) -> dict:
    if products_count > 15:
        limit = products_count
    else:
        limit = 15
    params = {
        'include_restrict': 'true',
        'limit': str(limit),
        'mode': 'store',
        'offset': '0',
    }
    return params
