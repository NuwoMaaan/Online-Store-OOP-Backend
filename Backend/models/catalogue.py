import json
from models.item import Item
from models.user import Customer

class Catalogue:
    __instance = None

    def __init__(self, data_file="Backend\db\mock_data.json"):
        if Catalogue.__instance is not None:
            raise Exception("Singleton class cannot be instantiated more than once.")

        self.items = self.load_items(data_file)
        Catalogue.__instance = self

    @staticmethod
    def get_instance():
        if Catalogue.__instance is None:
            Catalogue()
        return Catalogue.__instance

    def load_items(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        return [Item(**item) for item in data.get("items", [])]

    def get_all_items(self):
        return self.items

    def get_item_by_id(self, item_id):
        return next((item for item in self.items if item.item_id == item_id), None)
    
    def view_catalogue(self):
        print(f"------Catalogue------")
        #catalogue = Catalogue.get_instance()
        items = self.get_all_items()
        if not items:
            print("No items available in the catalogue.")
            return
        print("\nCatalogue Items:")
        for item in items:
            print(f"{item.item_id}: {item.name} - ${item.price:.2f}")
        

        # item_id = input("Enter item ID to add to cart (or 'q' to quit): ").strip()
        # if item_id.lower() == 'q':
        #     return menu(user)
        # else:
        #     try:
        #         item_id = int(item_id)
        #         item = self.get_item_by_id(item_id)
        #         if item:
        #             user.cart.add_item(item)
        #             print(f"Added {item.name} to your cart.")
        #             menu(user)
        #         else:
        #             print(f"Item with ID {item_id} not found in the catalogue.")
        #             menu(user)
        #     except ValueError:
        #         print("Invalid item ID. Please enter a valid number.")
        #         menu(user)
        
    
