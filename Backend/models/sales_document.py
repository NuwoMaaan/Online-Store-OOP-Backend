import datetime
import random
from models.order import Order
from models.format_items_table import print_items_table


class SalesDocument():
    def __init__(self):
        self.invoice_number = random.randint(6000,7000)
        self.date_time = datetime.datetime.now().replace(microsecond=0)
    
   
        

    def generate_sales_document(self, order):
        print("\n------Inoivce Receipt-------")
        print(f"Inoice Number: #{self.invoice_number}, Customer ID: {order.customer_id}")
        print(f"Date of processed: {self.date_time}, STATUS: {order.status}")
        print(f"Payment method: {type(order.payment).__name__} ")

        payment_attributes = vars(order.payment).items()
        for key, value in payment_attributes:
            display_key = key.replace('_', ' ')
            if display_key == 'card number':
                value = str(value)[-4:]
                print(f"Card ending in: ************{value}")
                continue
            print(f"{display_key}: {value}")
        print_items_table(order.items)
        print(f"Shipping address:"," ".join(str(value) for value in order.shipping_details.values()))

        print(f"Total: ${order.total}")


        

