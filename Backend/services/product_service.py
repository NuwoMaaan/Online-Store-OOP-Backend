# services/product_service.py

import json
from models.product import Product

# Handles product-related operations using object-oriented principles
class ProductService:
    def __init__(self, db_path="db/mock_data.json"):
        self.db_path = db_path
        self.products = self.load_products()

    # Loads product data and returns a list of Product objects (abstraction)
    def load_products(self):
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)
                return [Product.from_dict(prod) for prod in data.get("products", [])]
        except FileNotFoundError:
            return []

    # Saves current product list to file (encapsulation)
    def save_products(self):
        with open(self.db_path, "w") as f:
            json.dump({"products": [p.to_dict() for p in self.products]}, f, indent=4)

    def get_all_products(self):
        return self.products

    def get_product_by_id(self, product_id: int):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def add_product(self, product: Product):
        self.products.append(product)
        self.save_products()

    # Delegates stock logic to the Product class (responsibility separation)
    def reduce_stock(self, product_id: int, quantity: int):
        product = self.get_product_by_id(product_id)
        if product:
            product.reduce_stock(quantity)
            self.save_products()
            return product
        else:
            raise ValueError("Product not found.")
