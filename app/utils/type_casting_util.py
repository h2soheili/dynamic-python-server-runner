import enum
import types
import pandas as pd


def is_null(input: str):
    result = True
    if input is not None and str(input).strip() != 'null' and str(input).strip() != 'undefined':
        result = False
    return result


def to_int(input, replace_null_value=None) -> int:
    result = None
    if input != '' and input is not None and not pd.isnull(input) and not is_null(input):
        result = int(input)
    if result is None and replace_null_value is not None:
        result = replace_null_value
    return result


def to_str(input) -> str:
    result = ''
    if input is not None and not pd.isnull(input) and not is_null(input):
        result = str(input)
    return result


def to_float(input) -> float:
    result = None
    if input != '' and input is not None and not pd.isnull(input) and not is_null(input):
        result = float(input)
    return result


def to_bool(input) -> bool:
    result = input
    if input is not None:
        result = bool(input)
    return result


def to_dict(obj, skip_porps=None):
    if not hasattr(obj, "__dict__"):
        return obj
    if isinstance(obj, enum.Enum):
        return obj
    if skip_porps is None:
        skip_porps = list()
    result = {}
    for key in dir(obj):
        if key in skip_porps:
            continue
        if key.startswith("_"):
            continue
        val = getattr(obj, key)
        if type(val) == types.MethodType:
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(to_dict(item))
        else:
            element = to_dict(val)
        result[key] = element
    return result
