import json
from models.item import Item

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
    
    
