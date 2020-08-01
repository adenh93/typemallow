from marshmallow import Schema, fields, validate
from .mappings import mappings

__schemas = dict()
__enums = dict()

def ts_interface(context='default'):
    '''

    Any valid Marshmallow schemas with this class decorator will 
    be added to a list in a dictionary. An optional parameter: 'context'
    may be provided, which will create separate dictionary keys per context.
    Otherwise, all values will be inserted into a list with a key of 'default'.

    e.g.

    @ts_interface(context='internal')
    class Foo(Schema):
        first_field = fields.Integer()

    'context' can also be a list of strings, in this case the schema will be added to multiple contexts

    e.g.
    @ts_interface(context=['internal', 'external'])
    class Foo(Schema):
        first_field = fields.Integer()
    '''
    def decorator(cls):
        if issubclass(cls, Schema):
            if isinstance(context, list):
                for ctx in context:
                    if not ctx in __schemas:
                        __schemas[ctx] = []
                    __schemas[ctx].append(cls)
            else:
                if not context in __schemas:
                    __schemas[context] = []
                __schemas[context].append(cls)
        return cls

    return decorator


def _snake_to_pascal_case(key):
    '''
    Converts snake_case strings to PascalCase
    '''
    return ''.join(s for s in key.replace('_', ' ').title() if not s.isspace())


def _get_ts_type(value):
    if type(value) is fields.Nested:
        ts_type = value.nested.__name__
        if value.many:
            ts_type += '[]'
    elif type(value) is fields.List:
        item_type = value.container.__class__
        if item_type is fields.Nested:
            nested_type = value.container.nested.__name__
            ts_type = f'{nested_type}[]'
        else:
            type = mappings.get(item_type, 'any')
            ts_type = f'{type}[]'
    elif type(value) is fields.Dict:
        keys_type = mappings.get(type(value.key_container), 'any')
        values_type = _get_ts_type(value.value_container)
        ts_type = f'{{[key: {keys_type}]: {values_type}}}'
    else:
        ts_type = mappings.get(type(value), 'any')

    return ts_type


def _get_ts_interface(schema, context='default', strip_schema_keyword=False):
    '''

    Generates and returns a Typescript Interface by iterating
    through the declared Marshmallow fields of the Marshmallow Schema class
    passed in as a parameter, and mapping them to the appropriate Typescript
    data type.

    '''
    name = schema.__name__
    if strip_schema_keyword:
        name = name.replace('Schema', '')

    ts_fields = []

    for key, value in schema._declared_fields.items():
        if value.validate and type(value.validate) is validate.OneOf:
            # add to enums to be exported with _generate_enums_exports
            __enums[context] = {}
            __enums[context][_snake_to_pascal_case(key)] = value.validate.choices
            ts_type = _snake_to_pascal_case(key)
        else:
            ts_type = _get_ts_type(value)

        if value.allow_none:
            ts_type += '| null'

        if not value.required:
            key += '?'

        ts_fields.append(
            f'\t{key}: {ts_type};'
        )

    ts_fields = '\n'.join(ts_fields)
    return f'export interface {name} {{\n{ts_fields}\n}}\n\n'


def _generate_enums_exports(context='default'):
    '''
    Generates export statements for each enum found in schemas' with 'oneof' validations
    '''
    enum_exports = []
    for key, choices_tuple in __enums[context].iteritems():
        enum_fields = []
        for choice in choices_tuple:
            enum_fields.append(
                f'\t{choice.upper()} = "{choice}",'
            )
        enum_fields = '\n'.join(enum_fields)
        enum_exports.append(
            f'export enum {key} {{\n{enum_fields}\n}}'
        )

    if (len(enum_exports) > 0):
        return f'{enum_exports}\n\n'
    else:
        return ''


def generate_ts(output_path, context='default', strip_schema_keyword=False):
    '''

    When this function is called, a Typescript interface will be generated
    for each Marshmallow schema in the schemas dictionary, depending on the
    optional context parameter provided. If the parameter is ignored, all
    schemas in the default value, 'default' will be iterated over and a list
    of Typescript interfaces will be returned via a list comprehension.
    
    The Typescript interfaces will then be outputted to the file provided.

    The output file will also contain any enums found while iterating over the schemas.

    '''
    with open(output_path, 'w') as output_file:
        interfaces = [_get_ts_interface(schema, context, strip_schema_keyword) for schema in __schemas[context]]
        output_file.write(''.join(_generate_enums_exports(context)))
        output_file.write(''.join(interfaces))
