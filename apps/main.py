from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .filters.bloomfilter import BloomFilter

app = FastAPI()

# Initialize BloomFilter with expected number of items and false positive probability
bloom = BloomFilter(items_count=1000, fp_prob=0.01)

# Define a Pydantic model for item data validation
class ItemModel(BaseModel):
    item: str

# Route to add an item to the BloomFilter
@app.post("/add/")
async def add_item(item_data: ItemModel):
    item = item_data.item
    added = bloom.add(item)
    return {"message": "Item added", "added": added}

# Route to check if an item exists in the BloomFilter
@app.post("/check/")
async def check_item(item_data: ItemModel):
    item = item_data.item
    exists = bloom.check(item)
    return {"exists": exists}

# Exception handler for missing item
@app.exception_handler(HTTPException)
async def item_exception_handler(request, exc):
    return {"detail": str(exc.detail)}
