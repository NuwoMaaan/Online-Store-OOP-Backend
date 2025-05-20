# routes/product_routes.py

from fastapi import APIRouter, HTTPException
from services.product_service import ProductService
from models.product import Product

router = APIRouter()
product_service = ProductService()

@router.get("/", summary="Get all products")
def get_products():
    products = product_service.get_all_products()
    return [p.to_dict() for p in products]

@router.get("/{product_id}", summary="Get a product by ID")
def get_product(product_id: int):
    product = product_service.get_product_by_id(product_id)
    if product:
        return product.to_dict()
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/", summary="Add a new product")
def add_product(product: dict):
    try:
        new_product = Product.from_dict(product)
        product_service.add_product(new_product)
        return {"message": "Product added successfully", "product": new_product.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}/reduce-stock", summary="Reduce stock for a product")
def reduce_product_stock(product_id: int, quantity: int):
    try:
        updated_product = product_service.reduce_stock(product_id, quantity)
        return {
            "message": f"{quantity} item(s) deducted from stock.",
            "product": updated_product.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
