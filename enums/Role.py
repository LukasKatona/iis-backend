from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    FARMER = "farmer"
    CUSTOMER = "customer"
    GUEST = "guest"