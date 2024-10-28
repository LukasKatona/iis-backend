from enum import Enum

class CategoryRequestState(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
