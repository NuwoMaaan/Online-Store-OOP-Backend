from services.order_service import OrderService 
from services.payment_service import PaymentService
from services.sales_service import SalesService
from services.cart_service import CartService

class TransactionFacade():
    def __init__(self):
        self.order_service = OrderService()
        self.payment_service = PaymentService()
        self.sales_service = SalesService()
        self.cart_service = CartService()

    def process(self, user):
        order = self.order_service.checkout(user)
        if not order:
            return
            
        user.orders.append(order)
        payment = self.payment_service.process(order)
        if not payment:
            print("Transaction failed.")
            return

        order.add_payment(payment)
        if self.order_service.reduce_stock(order):
            if self.order_service.insert_order(order):
                self.sales_service.generate(order, payment)
                print("\nOrder completed successfully.")
        user.orders.clear()
        user.cart.clear_cart()