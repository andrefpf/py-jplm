import re
from collections import defaultdict

t_view_regex = re.compile(r"[0-9]+(?=_)")
s_view_regex = re.compile(r"(?<=_)[0-9]+")


def nested_dict():
    return defaultdict(nested_dict)


def view_position_from_name(view_name: str):
    t_found = t_view_regex.findall(view_name)
    s_found = s_view_regex.findall(view_name)

    if len(t_found) != 1:
        raise ValueError("Position T not found")

    if len(s_found) != 1:
        raise ValueError("Position S not found")

    try:
        t = int(t_found[0])
        s = int(s_found[0])

    except:
        raise ValueError("Unable to transform the position values in integers.")

    finally:
        return t, s
