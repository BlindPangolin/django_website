import os
import json


def env_var_to_bool(var_name, default=False):
    v = os.environ.get(var_name)
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    return v.upper() == 'TRUE'


def env_var_from_json_string(var_name, default=None):
    v = os.environ.get(var_name)
    if v is None:
        return default
    if isinstance(v, str):
        return json.loads(v)
    return default
