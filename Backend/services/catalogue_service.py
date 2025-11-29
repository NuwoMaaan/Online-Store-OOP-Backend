
import json
from models.item import Item


DATABASE_PATH = "Backend/db/mock/mock_data.json"

class CatalogueService():

    @staticmethod
    def remove_item(catalogue_instance):
        catalogue = catalogue_instance.get_instance()
        catalogue.view_catalogue()
        while True:
            item_id = input("Enter Item ID to remove (or 'q' to quit): ").strip().lower()
            if item_id == 'q':
                break
            try:
                item_id = int(item_id)
                remove_item = catalogue.get_item_by_id(item_id)
                if remove_item:
                    catalogue.items = [item for item in catalogue.items if item.item_id != item_id]
                    with open(DATABASE_PATH, "r") as f:
                        data = json.load(f)
                    db_items = data.get("items", [])
                    db_items = [item for item in db_items if int(item["item_id"]) != item_id]
                    data["items"] = db_items
                    with open(DATABASE_PATH, "w") as f:
                        json.dump(data, f, indent=4)
                    print(f"Removed Item ID: {item_id}")
                    break
                else:
                    print(f"Item with ID {item_id} not found.")
            except ValueError:
                print("Invalid item ID. Please enter a valid number or 'q' to quit.")
                
    @staticmethod
    def add_item(catalogue_instance):
        catalogue = catalogue_instance.get_instance()
        catalogue.view_catalogue()
        name = input("Enter item name: ")
        price = float(input("Enter item price: "))
        quantity = input("Enter item quantity: ") #quantity is not an attribute of Item and has no current functionality. i.e. does not decrement or checked at order processing.

        with open(DATABASE_PATH, "r") as f:
            data = json.load(f)
        items = data.get("items", [])
        last_id = data.get("total_history_id_count", 0) #ensures that element add has item_id + 1 of total historic elements, meaning no duplicated item_id even if Item has been removed.
        new_id = last_id + 1
        items.append({
            "item_id": new_id,
            "name": name,
            "price": price,
            "quantity": quantity
        })
        data["items"] = items
        data["total_history_id_count"] = new_id
        with open(DATABASE_PATH, "w") as f:
            json.dump(data, f, indent=4)
        print(f"\nItem '{name}' added to catalogue with ID {new_id}.")

        new_item_obj = Item(new_id, name, price)
        catalogue.items.append(new_item_obj) #this adds to it into (memory - catalogue.items = []) (Maybe redundant?)
            