# routes/order_routes.py

from fastapi import APIRouter, HTTPException
from services.order_service import OrderService

router = APIRouter()
order_service = OrderService()

@router.post("/place/{user_id}", summary="Place an order for the user")
def place_order(user_id: int):
    try:
        order = order_service.place_order(user_id)
        return {"message": "Order placed successfully", "order": order.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{order_id}", summary="Get an order by ID")
def get_order(order_id: int):
    order = order_service.get_order_by_id(order_id)
    if order:
        return order.to_dict()
    raise HTTPException(status_code=404, detail="Order not found")

@router.get("/user/{user_id}", summary="Get all orders by user")
def get_orders_by_user(user_id: int):
    orders = order_service.get_orders_by_user(user_id)
    return [o.to_dict() for o in orders]
