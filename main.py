# library imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import URL
from sqlmodel import Session, create_engine, select

# local imports
from entities.Product import ProductCategory

connection_string = URL.create(
    'postgresql',
    username='admin',
    password='pgtvTuwoV5G7',
    host='ep-wild-mode-a2zrk2og.eu-central-1.pg.koyeb.app',
    database='koyebdb',
)

db = create_engine(connection_string)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed, "*" allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust allowed methods (GET, POST, etc.)
    allow_headers=["*"],  # Adjust allowed headers
)

@app.get("/product-categories")
def get_product_categories() -> list[ProductCategory]:
    with Session(db) as session:
        return list(session.exec(select(ProductCategory)))

    
@app.get("/product-categories/{category_id}")
def get_product_category_by_id(category_id: int) -> ProductCategory:
    with Session(db) as session:
        return session.exec(select(ProductCategory).where(ProductCategory.id == category_id)).first()