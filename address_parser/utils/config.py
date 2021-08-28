import json

from pathlib import Path

SOURCE_PATH = Path(__file__).resolve()
PROJECT_DIR = SOURCE_PATH.parent.parent
JSON_DIR = PROJECT_DIR / "json"


def read_json_file(filepath):
    with open(filepath.resolve(), "r") as f:
        return json.load(f)


DIRECTIONS = read_json_file(JSON_DIR / "directions.json")
STREET_TYPES = read_json_file(JSON_DIR / "street_types.json")
OCCUPANCY_IDENTIFIERS = read_json_file(JSON_DIR / "occupancy_identifiers.json")
TRANSITIONS = read_json_file(JSON_DIR / "transitions.json")
DISPATCH_TABLE = {
                    'junk': lambda tkn: True,
                    'house_num': lambda tkn: tkn[0].isdigit(),
                    'pre_dir': lambda tkn: tkn in DIRECTIONS,
                    'str_nm': lambda tkn: True,
                    'str_type': lambda tkn: tkn in STREET_TYPES,
                    'post_dir': lambda tkn: tkn in DIRECTIONS,
                    'occ_id': lambda tkn: tkn in OCCUPANCY_IDENTIFIERS,
                    'occ_num': lambda tkn: True
                }
