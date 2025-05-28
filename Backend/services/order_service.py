from models.order import Order
from models.Saledoc import SalesDoc
from models.cart import Cart
from models.item import Item

class OrderService:
    def create_order_from_cart(self, cart_data, shipping_address, shipping_cost):
        cart = Cart(customer_id=cart_data["customer_id"])
        for item_data in cart_data["items"]:
            item = Item(item_id=item_data["item_id"], price=item_data["price"])
            cart.add_item(item)
        return Order.create_from_cart(cart, shipping_address, shipping_cost)

    def get_order(self, order_id):
        return Order.get_by_id(order_id)

    def generate_sales_doc(self, order_id):
        order = Order.get_by_id(order_id)
        total = order.calculate_total()
        return SalesDoc.create(order_id, order.customer_id, total)
