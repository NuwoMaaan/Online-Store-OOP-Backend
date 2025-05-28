
class SaleDocument():
    def __init__(self, sale_id, customer_id, sale_date, total_amount):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.sale_date = sale_date
        self.total_amount = total_amount

    def __repr__(self):
        return f"SaleDocument(sale_id={self.sale_id}, customer_id={self.customer_id}, sale_date={self.sale_date}, total_amount={self.total_amount})"
    