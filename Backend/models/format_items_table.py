

def print_items_table(items):
    if not items:
        print("No items to display.")
        return

    # Prepare for both object and dict items
    def get_attr(item, attr):
        # Try 'id', then 'item_id', then dict key, else ""
        if hasattr(item, attr):
            return getattr(item, attr)
        elif attr == "id" and hasattr(item, "item_id"):
            return getattr(item, "item_id")
        elif isinstance(item, dict):
            return item.get(attr, "") or item.get("item_id", "")
        else:
            return ""

    # Calculate max widths
    id_width = max(len(str(get_attr(item, "item_id"))) for item in items + [{"item_id": "ID"}])
    name_width = max(len(get_attr(item, "name")) for item in items + [{"name": "Name"}])
    price_width = max(len(f"{get_attr(item, 'price'):.2f}") for item in items if get_attr(item, "price") != "" or isinstance(get_attr(item, "price"), (int, float)))
    price_width = max(price_width, len("Price"))

    # Print header
    print(f"{'ID':<{id_width}}  {'Name':<{name_width}}  {'Price':>{price_width}}")
    # Print items
    for item in items:
        item_id = get_attr(item, "id")
        name = get_attr(item, "name")
        price = get_attr(item, "price")
        print(f"{item_id:<{id_width}}  {name:<{name_width}}  ${price:>{price_width}.2f}")