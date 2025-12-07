from db.repositories.item_repository import create_item, remove_item_catalogue

class CatalogueService():
    @staticmethod
    def remove_item(catalogue):
        catalogue.view_catalogue()
        while True:
            item_id = int(input("Enter Item ID to remove (or 'q' to quit): ").strip().lower())
            if item_id == 'q':
                break
            try:
                if remove_item_catalogue(item_id):
                    break
                else: 
                    print(f"Item with ID {item_id} not found.")
            except ValueError:
                print("Invalid item ID. Please enter a valid number or 'q' to quit.")
                
    @staticmethod
    def add_item(catalogue):
        catalogue.view_catalogue()
        name = input("Enter item name: ")
        price = float(input("Enter item price: "))
        quantity = int(input("Enter item quantity: "))

        new_id = create_item(name, price, quantity)
        if new_id:
            print(f"\nItem - '{name}' added to catalogue with ID - {new_id}.")

        # new_item_obj = Item(new_id, name, price)
        # catalogue.items.append(new_item_obj) 
            