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
    
    @staticmethod
    def strToEnum(status: str) -> 'OrderStatus':
        if status == "in_cart":
            return OrderStatus.IN_CART
        elif status == "pending":
            return OrderStatus.PENDING
        elif status == "accepted":
            return OrderStatus.ACCEPTED
        elif status == "rejected":
            return OrderStatus.REJECTED
        elif status == "cancelled":
            return OrderStatus.CANCELLED
        elif status == "shipped":
            return OrderStatus.SHIPPED
        elif status == "supplied":
            return OrderStatus.SUPPLIED
        elif status == "refunded":
            return OrderStatus.REFUNDED
        else:
            raise ValueError("Invalid role")
