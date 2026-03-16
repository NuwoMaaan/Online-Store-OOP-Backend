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

        payment = self.payment_service.process(order)
        if not payment:
            print("Transaction failed.")
            return

        with get_session() as db:
            shortages = self.order_service.check_stock(order, db)
            if shortages:
                if self.order_service.adjust_order(shortages):
                    self.order_service.adjust_order_for_shortages(order, shortages)

            success = self.order_service.reduce_stock(order, db)
            if not success:
                raise Exception("Stock changed during checkout. Please try again.")

            user.orders.append(order)
            order.add_payment(payment)

            if self.order_service.insert_order(order, db):
                self.sales_service.generate(order, payment)
                print("\nOrder completed successfully.")

            user.orders.clear()
            user.cart.clear_cart()

