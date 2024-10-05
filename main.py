# library imports
from typing import Union
from enum import Enum
from http.client import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa
from sqlalchemy import URL

# local imports
from entities.Product import Product, ProductCategory

connection_string = URL.create(
    'postgresql',
    username='admin',
    password='pgtvTuwoV5G7',
    host='ep-wild-mode-a2zrk2og.eu-central-1.pg.koyeb.app',
    database='koyebdb',
)

db = sa.create_engine(connection_string)
Session = sa.orm.sessionmaker(bind=db)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed, "*" allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust allowed methods (GET, POST, etc.)
    allow_headers=["*"],  # Adjust allowed headers
)

# DELETE THIS BLOCK v

# class Category(Enum):
#     TOOLS = "tools"
#     CONSUMABLES = "consumables"

# class Item(BaseModel):
#     name : str
#     price : float
#     count : int
#     id : int
#     category : Category

# generate list of 33 items
# items = {
#     0: Item(name="hammer", price=10.0, count=5, id=0, category=Category.TOOLS),
#     1: Item(name="nails", price=1.0, count=100, id=1, category=Category.CONSUMABLES),
#     2: Item(name="screwdriver", price=5.0, count=10, id=2, category=Category.TOOLS),
# }

# Selection = dict[
#     str, str | float | int | Category | None
# ]

# @app.get("/")
# def index() -> dict[str, dict[int, Item]]:
#     return {"items": items}

# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return items[item_id]

# @app.get("/items/")
# def get_items(
#     name: str | None = None,
#     price : float | None = None,
#     count : int | None = None,
#     category : Category | None = None
# ) -> dict[str, Selection]:
#     def check_item(item: Item) -> bool:
#         return all(
#             name is None or item.name == name,
#             price is None or item.price == price,
#             count is None or item.count != count,
#             category is None or item.category is category
#         )
#     selection = [item for item in items.values() if check_item(item)]
#     return {
#         "query": {"name": name, "price": price, "count": count, "category": category},
#         "selection": selection,
#     }

# DELETE THESE BLOCK ^

@app.get("/product-categories")
def get_product_categories() -> list[ProductCategory]:
    with Session() as session:
        return session.query(ProductCategory).all()