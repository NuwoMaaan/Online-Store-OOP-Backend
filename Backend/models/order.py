
from typing import List
from datetime import datetime
from services.order_service import OrderService


class Order:
    def __init__(self, customer_id, items, shipping_details):
        self.customer_id: int = customer_id
        self.items: List = items 
        self.shipping_details: dict[str, str] = shipping_details
        self.subtotal: int = sum(item.price for item in items)
        self.shipping_cost: int = 10
        self.total: float = self.subtotal + self.shipping_cost
        self.status: str = "pending"     # or "paid"
        self.payment = None              # IPayment object
        self.date_time: datetime = datetime.now()
        self.order_no: int = None        # to be set when saved to DB  
        

    def add_payment(self, payment):
        self.payment = payment
        self.status = "paid"

    def order_summary(self):
        OrderService.order_summary(self)


