
import json
from pathlib import Path

class SalesDoc:
    DATA_PATH = Path("database/sales_docs.json")

    def __init__(self, doc_id: int, order_id: int, customer_id: int, amount: float):
        self.id = doc_id
        self.order_id = order_id
        self.customer_id = customer_id
        self.amount = amount

    @classmethod
    def create(cls, order_id: int, customer_id: int, amount: float) -> "SalesDoc":
        if cls.DATA_PATH.exists():
            with open(cls.DATA_PATH, "r") as f:
                docs = json.load(f)
        else:
            docs = []

        new_id = len(docs) + 1
        new_doc = {
            "id": new_id,
            "order_id": order_id,
            "customer_id": customer_id,
            "amount": amount
        }
        docs.append(new_doc)

        with open(cls.DATA_PATH, "w") as f:
            json.dump(docs, f, indent=2)

        return cls(new_id, order_id, customer_id, amount)

    def __repr__(self):
        return f"<SalesDoc id={self.id} order_id={self.order_id} customer_id={self.customer_id} amount={self.amount:.2f}>"
