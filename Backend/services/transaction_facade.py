from services.order_service import OrderService 
from services.payment_service import PaymentService
from services.sales_service import SalesService
from services.cart_service import CartService
from db.connection.session import get_session

class TransactionFacade():
    def __init__(self):
        self.order_service = OrderService()
        self.payment_service = PaymentService()
        self.sales_service = SalesService()
        self.cart_service = CartService()

    def process(self, user) -> None:
        order = self.order_service.checkout(user)
        if not order:
            return
            
        user.orders.append(order)
        payment = self.payment_service.process(order)
        if not payment:
            print("Transaction failed.")
            return
        order.add_payment(payment)

        with get_session() as db:
            success = self.order_service.reduce_stock(order, db)
            if not success:
                raise Exception("Checkout cancelled")
            if self.order_service.insert_order(order, db):
                self.sales_service.generate(order, payment)
                print("\nOrder completed successfully.")

            user.orders.clear()
            user.cart.clear_cart()