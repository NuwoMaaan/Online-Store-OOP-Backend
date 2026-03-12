from db.repositories.item_repository import create_item, remove_item_catalogue, get_all_items_db
from db.connection.session import get_session
from models.item import Item

class CatalogueService():
    @staticmethod
    def remove_item(catalogue):
        with get_session() as db:
            catalogue.view_catalogue()
            while True:
                item_id = input("Enter Item ID to remove (or 'q' to quit): ").strip().lower()
                if item_id == 'q':
                    break
                try:
                    if remove_item_catalogue(int(item_id), db):
                        break
                    else: 
                        print(f"Item with ID {item_id} not found.")
                except ValueError:
                    print("Invalid item ID. Please enter a valid number or 'q' to quit.")
                    
    @staticmethod
    def add_item(catalogue):
        with get_session() as db:
            catalogue.view_catalogue()
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            quantity = int(input("Enter item quantity: "))
            new_id = create_item(name, price, quantity, db)
            if new_id:
                print(f"\nItem - '{name}' added to catalogue with ID - {new_id}, quantity: {quantity}.")

    @staticmethod
    def load_items() -> list[Item]:
        with get_session() as db:
            item_list = get_all_items_db(db)
            if not item_list:
                return []
        
            domain_items = []
            for orm_item in item_list:
                item = dict(orm_item)
                item.pop("quantity", None)
                item = Item(**item)
                domain_items.append(item)
            return domain_items
            