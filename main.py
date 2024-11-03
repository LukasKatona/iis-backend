# library imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local imports
from api import ProductCategoryApi, ProductApi, EventApi

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed, "*" allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust allowed methods (GET, POST, etc.)
    allow_headers=["*"],  # Adjust allowed headers
)

# Include routers
app.include_router(ProductCategoryApi.router)
app.include_router(ProductApi.router)
app.include_router(EventApi.router)