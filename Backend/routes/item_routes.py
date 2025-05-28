# routes/item_routes.py

from fastapi import APIRouter, HTTPException
from services.item_service import ItemService
from models.item import Item

router = APIRouter()
item_service = ItemService()

@router.get("/", summary="Get all items")
def get_items():
    items = item_service.get_all_items()
    return [p.to_dict() for p in items]

@router.get("/{item_id}", summary="Get a item by ID")
def get_item(item_id: str):
    item = item_service.get_item_by_id(item_id)
    if item:
        return item.to_dict()
    raise HTTPException(status_code=404, detail="item not found")

@router.post("/", summary="Add a new item")
def add_item(item: dict):
    try:
        new_item = item.from_dict(item)
        item_service.add_item(new_item)
        return {"message": "item added successfully", "item": new_item.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{item_id}/reduce-stock", summary="Reduce stock for a item")
def reduce_item_stock(item_id: str, quantity: int):
    try:
        updated_item = item_service.reduce_stock(item_id, quantity)
        return {
            "message": f"{quantity} item(s) deducted from stock.",
            "item": updated_item.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
