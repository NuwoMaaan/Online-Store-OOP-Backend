from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from services.cart_service import CartService

router = APIRouter()
cart_service = CartService()

class AddToCartRequest(BaseModel):
    user_id: int
    item_id: str
    price: float = Field(..., gt=0, description="Price must be positive")
    quantity: Optional[int] = Field(1, gt=0, description="Quantity must be at least 1")

class RemoveFromCartRequest(BaseModel):
    user_id: int
    item_id: str

class ClearCartRequest(BaseModel):
    user_id: int

@router.post("/add", summary="Add item to cart")
def add_to_cart(request: AddToCartRequest):
    try:
        cart = cart_service.add_to_cart(
            user_id=request.user_id,
            item_id=request.item_id,
            price=request.price,
            quantity=request.quantity or 1
        )
        return {"message": "item added to cart", "cart": cart.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/remove", summary="Remove item from cart")
def remove_from_cart(request: RemoveFromCartRequest):
    cart = cart_service.remove_from_cart(request.user_id, request.item_id)
    return {"message": "item removed from cart", "cart": cart.to_dict()}

@router.post("/clear", summary="Clear user's cart")
def clear_cart(request: ClearCartRequest):
    cart = cart_service.clear_user_cart(request.user_id)
    return {"message": "Cart cleared", "cart": cart.to_dict()}

@router.get("/{user_id}", summary="Get cart for a user")
def get_cart(user_id: int):
    cart = cart_service.get_cart_by_user_id(user_id)
    return cart.to_dict()
