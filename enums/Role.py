from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    FARMER = "farmer"
    CUSTOMER = "customer"
    GUEST = "guest"

    @staticmethod
    def strToEnum(role: str) -> 'Role':
        if role == "admin":
            return Role.ADMIN
        elif role == "moderator":
            return Role.MODERATOR
        elif role == "farmer":
            return Role.FARMER
        elif role == "customer":
            return Role.CUSTOMER
        elif role == "guest":
            return Role.GUEST
        else:
            raise ValueError("Invalid role")