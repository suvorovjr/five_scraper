from typing import List, Optional
from pydantic import BaseModel, Field


class SubcategoriesModel(BaseModel):
    id: str
    name: str
    products_count: int


class CategoryModel(BaseModel):
    id: str
    name: str
    products_count: int
    subcategories: List[SubcategoriesModel]


class ImageLinks(BaseModel):
    normal: List[str]


class RatingModel(BaseModel):
    rating_average: float
    rates_count: int


class LabelModel(BaseModel):
    label: str
    bg_color: str
    text_color: str


class PricesModel(BaseModel):
    regular_price: float = Field(alias='regular')
    sale_price: Optional[bool] = Field(alias='', default=None)
    promo_price: Optional[float] = Field(default=None, alias='cpd_promo_price')


class ProductModel(BaseModel):
    id: int = Field(alias='plu')
    name: str
    image_links: ImageLinks
    rating: RatingModel
    prices: PricesModel
    property_clarification: str
    measurement_unit: str = Field(alias='uom')
    quantity: float = Field(alias='step')
    labels: Optional[List[LabelModel]] = Field(default=None)


class ProductsListModel(BaseModel):
    name: str
    products: List[ProductModel]
