from typing import List
from models.item import Item
from utlities.format_items_table import print_items_table
from services.catalogue_service import CatalogueService
from db.repositories.item_repository import get_all_items_db

class Catalogue():
    __instance = None
    def __init__(self):
        if Catalogue.__instance is not None:
            raise Exception("Singleton class cannot be instantiated more than once.")
        self.items: List[Item] = self.load_items()
        Catalogue.__instance = self

    @staticmethod
    def get_instance():
        if Catalogue.__instance is None:
            Catalogue()
        return Catalogue.__instance

    def load_items(self) -> list[Item]:
        item_list = get_all_items_db()
        if item_list:
            items = []
            for item in item_list:
                # Dont include quantity to construct Item
                item_data = {k: v for k, v in item.items() if k != "quantity"}
                items.append(Item(**item_data))
            return items
    
    def get_item_by_id(self, item_id) -> Item | None:
        return next((item for item in self.items if item.id == item_id), None)
    
    def get_all_items(self) -> list[Item]:
        return self.items
    
    def view_catalogue(self):
        print(f"======Catalogue======")
        items = self.get_all_items()
        if not items:
            print("No items available in the catalogue.")
            return
        print_items_table(items)

    
    @staticmethod
    def catalogue_menu(user):
        catalogue = Catalogue.get_instance()
        while True:
            catalogue.view_catalogue()
            item_id = input("Enter item ID to add to cart (or 'q' to quit): ").strip()
            if item_id.lower() == 'q':
                break
            try:
                item_id = int(item_id)
                item = catalogue.get_item_by_id(item_id)
                if item:
                    user.cart.add_item(item)
                    print(f"Added {item.name} to your cart.")
                else:
                    print(f"Item with ID {item_id} not found in the catalogue.")
            except ValueError:
                print("Invalid item ID. Please enter a valid number or 'q' to quit.")
    
    @staticmethod
    def catalogue_staff():
        catalogue = Catalogue.get_instance() 
        while True:
            choice = input("\n1 - 'add' new Item\n2 - 'remove' Item\nq - quit\nchoice: ").strip().lower()
            if choice == 'q':
                break
            elif choice == '1':
                CatalogueService.add_item(catalogue) 
            elif choice == '2':
                CatalogueService.remove_item(catalogue)
        


