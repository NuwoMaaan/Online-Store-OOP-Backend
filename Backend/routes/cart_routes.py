

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.cart_service import CartService

router = APIRouter()
cart_service = CartService()

class AddToCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class RemoveFromCartRequest(BaseModel):
    user_id: int
    product_id: int

class ClearCartRequest(BaseModel):
    user_id: int

@router.post("/add", summary="Add product to cart")
def add_to_cart(request: AddToCartRequest):
    cart = cart_service.add_to_cart(request.user_id, request.product_id, request.quantity)
    return {"message": "Product added to cart", "cart": cart.to_dict()}

@router.post("/remove", summary="Remove product from cart")
def remove_from_cart(request: RemoveFromCartRequest):
    cart = cart_service.remove_from_cart(request.user_id, request.product_id)
    return {"message": "Product removed from cart", "cart": cart.to_dict()}

@router.post("/clear", summary="Clear user's cart")
def clear_cart(request: ClearCartRequest):
    cart = cart_service.clear_user_cart(request.user_id)
    return {"message": "Cart cleared", "cart": cart.to_dict()}

@router.get("/{user_id}", summary="Get cart for a user")
def get_cart(user_id: int):
    cart = cart_service.get_cart_by_user_id(user_id)
    return cart.to_dict()

