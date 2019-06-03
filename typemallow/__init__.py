from marshmallow import Schema
from .mappings import MAPPINGS

__schemas = dict()

def ts_interface(context='default'):
    def decorator(cls):
        if issubclass(cls, Schema):
            if not context in __schemas:
                __schemas[context] = []
            __schemas[context].append(cls)
        return cls
    return decorator


def __get_ts_interface(schema):
    pass


def generate_ts(output_path, context='default'):
    interfaces = [__get_ts_interface(schema) for schema in __schemas]
    with open(output_path) as output_file:
        output_file.write(''.join(interfaces))