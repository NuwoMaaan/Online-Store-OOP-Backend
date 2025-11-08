
class SalesService:
    @staticmethod
    def generate(order, payment):
        doc = payment.create_salesdocument()
        doc.generate_sales_document(order)