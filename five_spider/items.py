import scrapy


class ProductItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    regular_price = scrapy.Field()
    sale_price = scrapy.Field()
    promo_price = scrapy.Field()
    review_count = scrapy.Field()
    rating = scrapy.Field()
    image_links = scrapy.Field()
    property_clarification = scrapy.Field()
    measurement_unit = scrapy.Field()
    quantity = scrapy.Field()
    promo = scrapy.Field()
