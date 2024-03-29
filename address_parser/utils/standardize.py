from .config import DIRECTIONS, STREET_TYPES, OCCUPANCY_IDENTIFIERS


def standardize_street_type(str_type: str) -> str:
    """
    Standardizes Street Types

    :param str_type: Street Type Label
    :type str_type: str
    :return: Standardized Street Type (e.g. 'AVENUE' -> 'AVE')
    :rtype: str
    """
    return STREET_TYPES.get(str_type, '')


def standardize_direction(direction: str) -> str:
    """
    Standardizes Street Directions

    :param direction: Pre/Post Direction Label
    :type direction: str
    :return: Standardized Direction (e.g. 'NORTHEAST' -> 'NE')
    :rtype: str
    """
    return DIRECTIONS.get(direction, '')


def standardize_occupancy_identifier(occ_id: str) -> str:
    """
    Standardizes Occupancy Identifiers

    :param direction: Occupancy Identifier Label
    :type direction: str
    :return: Standardized Occupancy Identifier (e.g. 'SUITE' -> 'STE')
    :rtype: str
    """
    return OCCUPANCY_IDENTIFIERS.get(occ_id, '')
