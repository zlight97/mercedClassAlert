import json
from collections import namedtuple

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

# Parse JSON into an object with attributes corresponding to dict keys.
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

x = json2obj(data)
print x.name, x.hometown.name, x.hometown.id