from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from services.order_service import OrderService
from models.item import Item

router = APIRouter()
service = OrderService()

class CartData(BaseModel):
    customer_id: int
    items: List[Item]

class OrderRequest(BaseModel):
    cart: CartData
    shipping_address: str
    shipping_cost: float

@router.post("/orders")
def create_order(order: OrderRequest):
    try:
        new_order = service.create_order_from_cart(
            cart_data=order.cart.model_dump(),
            shipping_address=order.shipping_address,
            shipping_cost=order.shipping_cost
        )
        return {"order_id": new_order.order_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/orders/{order_id}/salesdoc")
def generate_sales_doc(order_id: int):
    try:
        doc = service.generate_sales_doc(order_id)
        return {"sales_doc_id": doc.id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
