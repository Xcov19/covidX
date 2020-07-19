import enum


class EnumChoice(enum.Enum):
    """Generic Enum class to fill choices in model fields."""

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def choices(cls):
        return [(field.name, field.value) for field in cls]
