import uuid

from Backend.Service.DataObjects.product_data import ProductData
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct


class Product(IProduct):
    def __init__(self, product_name: str, price: float):
        self.product_name = product_name
        self.price = price
        self.id = str(self.id_generator())

    def parse(self):
        return ProductData(self.id, self.product_name, self.price)

    def set_product_name(self, new_name):
        self.product_name = new_name

    def get_id(self):
        return self.id

    def get_price(self):
        return self.price

    def get_name(self):
        return self.product_name

    def id_generator(self):
        return uuid.uuid4()

    def edit_product_details(self, product_name: str, price: float):
        self.product_name = product_name
        self.price = price
