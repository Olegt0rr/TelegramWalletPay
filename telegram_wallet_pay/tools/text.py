ENCODING = "utf-8"


def from_snake_to_pascal(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def from_snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    if "_" not in snake_str:
        return snake_str
    camel_string = from_snake_to_pascal(snake_str)
    return snake_str[0].lower() + camel_string[1:]
