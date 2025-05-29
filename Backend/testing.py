
from models.user import Customer
from models.catalogue import Catalogue
from models.cart import Cart

def main():
    # Create a customer
    customer = Customer(user_id=1, name="Leo", email="leo@outlook.com", role="customer")
    print(f"Customer created: {customer.name} (ID: {customer.user_id})\n")

    # Get items from Catalogue
    catalogue = Catalogue.get_instance()
    item1 = catalogue.get_item_by_id(1)
    item2 = catalogue.get_item_by_id(3)

    # Customer adds items to cart
    customer.cart.add_item(item1)
    customer.cart.add_item(item2)

    print("Items in cart:")
    for item in customer.cart.items:
        print(f"- {item.name}: ${item.price}")

    # Checkout
    order = customer.cart.checkout()

    print("\nOrder created:")
    print(f"Customer ID: {order['customer_id']}")
    for item in order['items']:
        print(f"- {item['name']}: ${item['price']}")
    print(f"Total: ${order['total']:.2f}")

if __name__ == "__main__":
    main()
