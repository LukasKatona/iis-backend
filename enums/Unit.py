from enum import Enum

class Unit(Enum):
    KILOGRAM = "kg"
    LITER = "l"
    PIECE = "piece"

    @staticmethod
    def strToEnum(unit: str) -> 'Unit':
        if unit == "kg":
            return Unit.KILOGRAM
        elif unit == "l":
            return Unit.LITER
        elif unit == "piece":
            return Unit.PIECE
        else:
            raise ValueError("Invalid unit")