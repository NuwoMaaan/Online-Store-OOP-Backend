from models.order import Order
from models.Saledoc import SalesDoc

class PaymentService:
    def __init__(self, PaymentMFactory):
        self.PaymentMfactory = PaymentMFactory

    def process_payment(self, data: dict):

        order_id = data.pop("order_id")
        order = Order.get_by_id(order_id)
        amount = order.calculate_total()
        data["amount"] = amount


        payment = self.PaymentMfactory.create_payment(**data)
        payment.validate()
        payment.pay()

        return SalesDoc.create(order_id=order_id, amount=amount)