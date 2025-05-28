
import json
from models.item import Item

# Handles item-related operations using object-oriented principles
class ItemService:
    def __init__(self, db_path="db/mock_data.json"):
        self.db_path = db_path
        self.items = self.load_items()

    # Loads item data and returns a list of item objects (abstraction)
    def load_items(self):
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)
                return [Item.from_dict(prod) for prod in data.get("items", [])]
        except FileNotFoundError:
            return []

    # Saves current item list to file (encapsulation)
    def save_items(self):
        with open(self.db_path, "w") as f:
            json.dump({"items": [p.to_dict() for p in self.items]}, f, indent=4)

    def get_all_items(self):
        return self.items

    def get_item_by_id(self, item_id: int):
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def add_item(self, item: Item):
        self.items.append(item)
        self.save_items()

    # Delegates stock logic to the item class (responsibility separation)
    def reduce_stock(self, item_id: int, quantity: int):
        item = self.get_item_by_id(item_id)
        if item:
            item.reduce_stock(quantity)
            self.save_items()
            return item
        else:
            raise ValueError("item not found.")
