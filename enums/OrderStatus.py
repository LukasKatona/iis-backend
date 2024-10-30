from enum import Enum

class OrderStatus(Enum):
    IN_CART = "in_cart"

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

    SHIPPED = "shipped"
    SUPPLIED = "supplied"

    REFUNDED = "refunded"
