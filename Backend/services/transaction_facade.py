
class TransactionFacade:
    def __init__(self, order_service, payment_service, sales_service, cart_service):
        self.order_service = order_service
        self.payment_service = payment_service
        self.sales_service = sales_service
        self.cart_service = cart_service

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