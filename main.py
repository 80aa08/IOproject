import random
from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = inventory = {
    "1": {"name": "Random Item 1", "price": 8.69, "brand": "Brand C"},
    "2": {"name": "Random Item 2", "price": 43.09, "brand": "Brand A"},
    "3": {"name": "Random Item 3", "price": 28.27, "brand": "Brand B"},
    "4": {"name": "Random Item 4", "price": 81.08, "brand": "Brand B"},
    "5": {"name": "Random Item 5", "price": 40.47, "brand": "Brand A"},
    "6": {"name": "Random Item 6", "price": 80.03, "brand": "Brand A"},
    "7": {"name": "Random Item 7", "price": 80.45, "brand": "Brand A"},
    "8": {"name": "Random Item 8", "price": 79.27, "brand": "Brand C"},
    "9": {"name": "Random Item 9", "price": 34.55, "brand": "Brand A"},
    "10": {"name": "Random Item 10", "price": 13.42, "brand": "Brand A"},
    "11": {"name": "Random Item 11", "price": 34.74, "brand": "Brand B"},
    "12": {"name": "Random Item 12", "price": 83.15, "brand": "Brand C"},
    "13": {"name": "Random Item 13", "price": 68.47, "brand": "Brand C"},
    "14": {"name": "Random Item 14", "price": 23.74, "brand": "Brand B"},
    "15": {"name": "Random Item 15", "price": 21.93, "brand": "Brand B"},
    "16": {"name": "Random Item 16", "price": 58.9, "brand": "Brand B"},
    "17": {"name": "Random Item 17", "price": 85.12, "brand": "Brand C"},
    "18": {"name": "Random Item 18", "price": 16.22, "brand": "Brand A"},
    "19": {"name": "Random Item 19", "price": 80.12, "brand": "Brand B"},
    "20": {"name": "Random Item 20", "price": 45.87, "brand": "Brand A"},
    "21": {"name": "Random Item 21", "price": 40.12, "brand": "Brand B"},
    "22": {"name": "Random Item 22", "price": 54.18, "brand": "Brand C"},
    "23": {"name": "Random Item 23", "price": 35.11, "brand": "Brand A"},
    "24": {"name": "Random Item 24", "price": 51.18, "brand": "Brand B"},
    "25": {"name": "Random Item 25", "price": 39.85, "brand": "Brand B"}
}

current_item_id = len(inventory) + 1

@app.get("/")
def get_all_items():
    if len(inventory) == 0:
        return {"Error": "No items added"}
    return inventory

@app.get("/get-by-id/{item_id}")
def get_item(item_id: int = Path(..., description="The ID of the item", gt=0)):
    str_item_id = str(item_id)
    if str_item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID not found")
    return inventory[str_item_id]

@app.get("/get-by-name/{name}")
def get_item_by_name(name: str):
    found_items = []
    for item_id, item in inventory.items():
        if name.lower() in item["name"].lower():
            found_items.append({"item_id": item_id, "item": item})

    if not found_items:
        raise HTTPException(status_code=404, detail="No items matching the name were found")

    return found_items


@app.post("/create-item/")
def create_item(item: Item):
    global current_item_id
    inventory[current_item_id] = item
    current_item_id += 1
    return {"item_id": current_item_id - 1, "item": item}

@app.post("/generate-items/{num_items}")
def generate_items(num_items: int):
    global current_item_id
    generated_items = []

    for _ in range(num_items):
        item = Item(
            name=f"Random Item {current_item_id}",
            price=round(random.uniform(1.0, 100.0),2),
            brand=random.choice(["Brand A", "Brand B", "Brand C"])
        )
        inventory[current_item_id] = item
        generated_items.append({"item_id": current_item_id, "item": item})
        current_item_id += 1

    return {"message": f"Generated {num_items} items", "generated_items": generated_items}

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    str_item_id = str(item_id)
    if str_item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")

    updated_item = inventory[str_item_id]

    for field, value in item.dict().items():
        if value is not None and value != updated_item.get(field):
            updated_item[field] = value

    return {"item_id": str_item_id, "item": updated_item}

@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)):
    str_item_id = str(item_id)
    if str_item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")
    del inventory[str_item_id]
    return {"Success": "Item deleted!"}

@app.delete("/delete-all-items")
def delete_item():
    if len(inventory)==0:
        return {"Error": "No items added"}

    inventory.clear()
    return {"Success": "All items deleted!"}

@app.get("/{path:path}")
def handle_default_path():
    return RedirectResponse("/")