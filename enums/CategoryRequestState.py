from enum import Enum

class CategoryRequestState(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    @staticmethod
    def strToEnum(state: str) -> 'CategoryRequestState':
        if state == "pending":
            return CategoryRequestState.PENDING
        elif state == "approved":
            return CategoryRequestState.APPROVED
        elif state == "rejected":
            return CategoryRequestState.REJECTED
        else:
            raise ValueError("Invalid role")
