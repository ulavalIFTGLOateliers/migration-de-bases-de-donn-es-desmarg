import json
import os


def failable(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return False

    return wrapper


def load_db_states_from_json():
    json_file = "target.json"
    current_dir = os.path.dirname(__file__)
    abs_json_file_path = os.path.join(current_dir, json_file)

    with open(abs_json_file_path) as f:
        db_states = json.load(f)

    return db_states
