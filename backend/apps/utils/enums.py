from enum import Enum


class ChoicesEnum(Enum):
    """ Enum for model char field choice constants."""

    @classmethod
    def get_choices(cls) -> list:
        choices = []
        for prop in cls:
            choices.append((prop.value, prop.name))
        return choices
