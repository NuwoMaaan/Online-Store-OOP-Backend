import datetime
import random
from utlities.format_items_table import print_items_table


class SalesDocument():

    def generate_sales_document(self, order):
        print("\n------Inoivce Receipt-------")
        print(f"Inoice Number: #{order.order_no}, Customer ID: {order.customer_id}")
        print(f"Date of processed: {order.date_time}, STATUS: {order.status}")
        print(f"Payment method: {type(order.payment).__name__} ")

        payment_attributes = vars(order.payment).items()
        for key, value in payment_attributes:
            display_key = key.replace('_', ' ')
            if display_key == 'card number':
                value = str(value)[-4:]
                print(f"Card ending in: ************{value}")
                continue                                        
            if display_key == 'expiry date':
                continue
            print(f"{display_key}: {value}")
        print_items_table(order.items)
        print(f"Shipping address:"," ".join(str(value) for value in order.shipping_details.values()))

        print(f"Total: ${order.total:.2f}")
        print("Thank you for your purchase!")
       


        

