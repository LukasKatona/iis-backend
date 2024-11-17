# library imports
from typing import Union
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# local imports
from api import ProductCategoryApi, ProductApi, EventApi, UserApi, FarmerApi, ReviewApi, OrderApi, NewCategoryRequestApi
from enums.Role import Role
import auth

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
app.include_router(auth.router)
app.include_router(ProductCategoryApi.router)
app.include_router(ProductApi.router)
app.include_router(EventApi.router)
app.include_router(UserApi.router)
app.include_router(FarmerApi.router)
app.include_router(ReviewApi.router)
app.include_router(OrderApi.router)
app.include_router(NewCategoryRequestApi.router)

admin_api_list = [
    ("GET", "/users"),
    ("GET", "/users/{user_id}"),
    ("POST", "/users"),
    ("PATCH", "/users/{user_id}/update-role"),
    ("DELETE", "/users/{user_id}"),
]

moderator_api_list = [
    ("POST", "/product-categories"),
    ("PATCH", "/product-categories/{category_id}"),
    ("DELETE", "/product-categories/{category_id}"),

    ("PATCH", "/category-requests/{category_id}"),
    ("DELETE", "/category-requests/{category_id}"),
]

farmer_api_list = [
    ("POST", "/products"),
    ("PATCH", "/products/{product_id}"),
    ("DELETE", "/products/{product_id}"),

    ("POST", "/events"),
    ("PATCH", "/events/{event_id}"),
    ("DELETE", "/events/{event_id}"),
]

user_api_list = [
    ("GET", "/orders"),
    ("PATCH", "/orders/{order_id}/status"),
    ("POST", "/orders/add-product"),
    ("PATCH", "/orders/{order_id}/edit-product"),
    ("DELETE", "/orders/{order_id}"),
    ("DELETE", "/orders/{order_id}/product/{product_id}"),

    ("GET", "/category-requests"),
    ("POST", "/category-requests"),

    ("GET", "/farmers"),
    ("GET", "/farmers/{farmer_id}"),
    ("GET", "/farmers/{user_id}/by-user-id"),
    ("POST", "/farmers"),
    ("PATCH", "/farmers/{farmer_id}"),
    ("DELETE", "/farmers/{farmer_id}"),

    ("GET", "/events"),
    ("GET", "/events/{user_id}"),
    ("POST", "/events/{event_id}/join/{user_id}"),
    ("DELETE", "/events/{event_id}/leave/{user_id}"),

    ("GET", "/users/me"),
    ("PATCH", "/users/{user_id}"),
    ("PATCH", "/users/{user_id}/password"),

    ("GET", "/reviews"),
    ("POST", "/reviews/order/{order_id}"),
    ("POST", "/reviews/product/{product_id}"),
    ("DELETE", "/reviews/{review_id}"),
]

guest_api_list = [
    ("GET", "/products"),
    ("GET", "/products/{product_id}"),
    
    ("GET", "/product-categories"),
]

def get_access_level(request: Request) -> Union[Role, None]:
    if (request.method, request.url.path) in admin_api_list:
        return Role.ADMIN
    elif (request.method, request.url.path) in moderator_api_list:
        return Role.MODERATOR
    elif (request.method, request.url.path) in farmer_api_list:
        return Role.FARMER
    elif (request.method, request.url.path) in user_api_list:
        return Role.CUSTOMER
    elif (request.method, request.url.path) in guest_api_list:
        return Role.GUEST
    else:
        return None


@app.middleware("http")
async def process_requests(request: Request, call_next):
    response = await call_next(request)
    return response