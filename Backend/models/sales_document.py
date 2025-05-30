import datetime
import random
from models.order import Order


class SalesDocument():
    def __init__(self):
        self.invoice_number = random.randint(6000,7000)
        self.date_time = datetime.datetime.now()
    
   
        

    def generate_sales_document(self, order):
        print("\n-----Inoivce Receipt------")
        print(f"Inoice Number: {self.invoice_number}, Customer ID: {order.customer_id}")
        print(f"Date of processed: {self.date_time}, STATUS: {order.status}")
        print(f"Payment method: {type(order.payment).__name__} ")

        payment_attributes = vars(order.payment).items()
        for key,value in payment_attributes:
            print(f"{key}: {value}")
        for item in order.items:
            print(f"{item.name} - ${item.price:.2f}")
        print(f"Shipping address:"," ".join(str(value) for value in order.shipping_details.values()))

        print(f"Total: ${order.total}")


    

