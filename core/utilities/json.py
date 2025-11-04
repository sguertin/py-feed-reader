import json
from json import JSONEncoder
from pathlib import Path
def custom_json(obj):
    if isinstance(obj, complex):
        return {'__complex__': True, 'real': obj.real, 'imag': obj.imag}
    raise TypeError(f'Cannot serialize object of {type(obj)}')

class PathEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)

def read_json_file(file_path: Path)->dict[str,str]:
    with open(file_path, 'r') as f:
        return json.load(f)
    
def write_json_file(file_path: Path, object: dict[str,str]):
    with open(file_path, 'w+') as f:
        json.dump(object, f, cls=PathEncoder)
