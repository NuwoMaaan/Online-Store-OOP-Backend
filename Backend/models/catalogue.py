import json
from models.item import Item
from models.format_items_table import print_items_table

data_file = "Backend\db\mock_data.json"

class Catalogue:
    __instance = None
    def __init__(self, data_file = "Backend\db\mock_data.json"):
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
        items = []
        for item in data.get("items", []):
            # Dont include quantity to construct Item
            item_data = {k: v for k, v in item.items() if k != "quantity"}
            items.append(Item(**item_data))
        return items
    
    def get_item_by_id(self, item_id):
        return next((item for item in self.items if item.item_id == item_id), None)
    
    def get_all_items(self):
        return self.items
    
    def view_catalogue(self):
        print(f"======Catalogue======")
        items = self.get_all_items()
        if not items:
            print("No items available in the catalogue.")
            return
        #print("Catalogue Items:")
        # for item in items:
        #     print(f"{item.item_id}: {item.name} - ${item.price:.2f}")
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
    def catalogue_staff(user):
        catalogue = Catalogue.get_instance()
        while True:
            catalogue.view_catalogue()
            choice = input("\n1 - 'add' new Item\n2 - 'remove' Item\nq - quit\nchoice: ").strip().lower()
            if choice == 'q':
                break
            elif choice == '1':
                catalogue.add_item()
        
        

    def add_item(self):
        # with open(self.data_file, 'r') as f:
        #     data = json.load(f)
        #     items = data.get("items", [])
        items = self.get_all_items()
        if items:
            max_id = max(item.item_id for item in items)
            new_id = max_id + 1
        else:
            new_id = 1 #if there are no items in DB

        name = input("Enter item name: ")
        price = float(input("Enter item price: "))
        quantity = input("Enter item quantity: ") #quantity is not an attribute of Item and has not current functionality. i.e. does not decrement or checked at order processing.
        new_item_obj = Item(new_id, name, price)
        self.items.append(new_item_obj) #this adds to it into (memory - self.items = [])
        #write to db
        with open(data_file, "r") as f:
            data = json.load(f)
        db_items = data.get("items", [])
        db_items.append({
            "item_id": new_id,
            "name": name,
            "price": price,
            "quantity": quantity
        })
        data["items"] = db_items
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"\nItem '{name}' added to catalogue with ID {new_id}.")
            
        


