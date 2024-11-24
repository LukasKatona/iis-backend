# library imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local imports
from api import ProductCategoryApi, ProductApi, EventApi, UserApi, FarmerApi, ReviewApi, OrderApi, NewCategoryRequestApi
import auth

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://www.stud.fit.vutbr.cz",
        "http://www.stud.fit.vutbr.cz",   
        "https://www.stud.fit.vutbr.cz/~xkaton00/#/*",
        "http://www.stud.fit.vutbr.cz/~xkaton00/#/*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(ProductCategoryApi.router)
app.include_router(ProductApi.router)
app.include_router(EventApi.router)
app.include_router(UserApi.router)
app.include_router(FarmerApi.router)
app.include_router(ReviewApi.router)
app.include_router(OrderApi.router)
app.include_router(NewCategoryRequestApi.router)
