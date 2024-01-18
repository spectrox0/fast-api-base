""" Utils for messages """


def not_entity_found(entity: str) -> str:
    """
    Returns a string indicating that the specified entity was not found.

    Args:
        entity (str): The name of the entity that was not found.

    Returns:
        str: A string indicating that the entity was not found.
    """
    return f"{entity} not found"


def not_entities_found(entity: str) -> str:
    """
    Returns a string indicating that the specified entities were not found.

    Args:
        entity (str): The name of the entity that was not found.

    Returns:
        str: A string indicating that the entities were not found.
    """
    return f"No {entity} found"
