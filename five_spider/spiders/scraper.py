import json
from typing import Iterable
from urllib.parse import urlencode
from pydantic import ValidationError
from common.schemas import CategoryModel, ProductsListModel
from common.utils import get_headers, get_products_params, get_category_params
from ..items import ProductItem
import scrapy
from scrapy import Request


class ScraperSpider(scrapy.Spider):
    name = 'scraper'

    def __init__(self, shop_id: str):
        super().__init__()
        self.shop_id = shop_id

    def start_requests(self) -> Iterable[Request]:
        base_url = f'https://5d.5ka.ru/api/catalog/v1/stores/{self.shop_id}/categories'
        params = urlencode(get_category_params())
        url = f'{base_url}?{params}'
        headers = get_headers(self.shop_id)
        yield scrapy.Request(
            url=url,
            method='GET',
            headers=headers,
            callback=self.parse_categories
        )

    def parse_categories(self, response):
        response_data = response.json()
        categories = [CategoryModel(**category) for category in response_data]
        subcategories = []
        for category in categories:
            subcategories.extend(category.subcategories)
        self.logger.info(f"Всего категорий собрано: {len(subcategories)}")
        for subcategory in subcategories:
            base_url = f'https://5d.5ka.ru/api/catalog/v2/stores/{self.shop_id}/categories/{subcategory.id}/products'
            params = urlencode(get_products_params(subcategory.products_count))
            url = f'{base_url}?{params}'
            headers = get_headers(self.shop_id)
            self.logger.info(f"Отправляю запрос {subcategory.name}. В ней {subcategory.products_count} продуктов")
            yield scrapy.Request(
                url=url,
                method='GET',
                headers=headers,
                callback=self.parse_products,
                meta={'category_name': subcategory.name},
            )

    def parse_products(self, response):
        category_name = response.meta.get('category_name', 'unknown_category')
        try:
            response_data = response.json()
            products = ProductsListModel(**response_data)
        except json.JSONDecodeError as e:
            self.logger.error(f'JSONDecodeError: {e}. Retrying...')
            yield response.request.replace(dont_filter=True)
            return
        except ValidationError as e:
            self.logger.error(f'ValidationError: {e}. Retrying...')
            yield response.request.replace(dont_filter=True)
            return
        for product in products.products:
            product_item = ProductItem()
            product_item['id'] = product.id
            product_item['name'] = product.name
            product_item['regular_price'] = product.prices.regular_price
            product_item['sale_price'] = product.prices.sale_price
            product_item['promo_price'] = product.prices.promo_price
            product_item['review_count'] = product.rating.rates_count
            product_item['rating'] = product.rating.rating_average
            product_item['image_links'] = product.image_links.normal
            product_item['property_clarification'] = product.property_clarification
            product_item['measurement_unit'] = product.measurement_unit
            product_item['quantity'] = product.quantity
            if product.labels is not None:
                product_item['promo'] = product.labels[0].label
            yield product_item
        self.log_category(category_name)

    def log_category(self, category_name):
        self.logger.info(f'Категория {category_name} успешно обработана.')
        with open('processed_categories.txt', 'a') as f:
            f.write(f'{category_name}\n')
