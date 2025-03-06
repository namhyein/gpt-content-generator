import json


def serialize(obj):
    return json.dumps(obj, indent=4, sort_keys=True)


def deserialize(obj):
    return json.loads(obj)
