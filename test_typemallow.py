import unittest

from marshmallow import Schema, fields
from marshmallow.validate import OneOf

import typemallow

class TestTypemallow(unittest.TestCase):
    def test_snake_to_pascal_case(self):
        res = typemallow._snake_to_pascal_case('test_key')
        self.assertEquals(res, 'TestKey')

    def test_get_ts_type_string(self):
        res = typemallow._get_ts_type(fields.String())
        self.assertEquals(res, 'string')

    def test_get_ts_type_nested(self):
        class InternalSchema(Schema):
            stringField = fields.String()

        res = typemallow._get_ts_type(fields.Nested(InternalSchema))

        self.assertEquals(res, 'InternalSchema')

    def test_get_ts_type_nested_array(self):
        class InternalSchema(Schema):
            stringField = fields.String()

        res = typemallow._get_ts_type(fields.Nested(InternalSchema, many=True))

        self.assertEquals(res, 'InternalSchema[]')

    def test_get_ts_type_list(self):
        res = typemallow._get_ts_type(fields.List(fields.String(), required=False))

        self.assertEquals(res, 'string[]')

    def test_get_ts_type_list_of_nested(self):
        class InternalSchema(Schema):
            stringField = fields.String()

        res = typemallow._get_ts_type(fields.List(fields.Nested(InternalSchema)))

        self.assertEquals(res, 'InternalSchema[]')

    def test_get_ts_type_dict(self):
        res = typemallow._get_ts_type(fields.Dict(keys=fields.String(), values=fields.Integer()))

        self.assertEquals(res, '{[key: string]: number}')

    def test_get_ts_interface_not_stripped(self):
        choices = ['lorem', 'ipsum', 'dolor']

        class TestSchema(Schema):
            string_field = fields.String(required=True, allow_none=True)
            enum_field = fields.String(validate=OneOf(choices=choices))

        res = typemallow._get_ts_interface(TestSchema)

        self.assertEquals(res,
'''export interface TestSchema {
\tenum_field?: EnumField;
\tstring_field: string| null;
}

''')

    def test_get_ts_interface_stripped(self):
        choices = ['lorem', 'ipsum', 'dolor']

        class TestSchema(Schema):
            string_field = fields.String(required=True, allow_none=True)
            enum_field = fields.String(validate=OneOf(choices=choices))

        res = typemallow._get_ts_interface(TestSchema, strip_schema_keyword=True)

        self.assertEquals(res,
'''export interface Test {
\tenum_field?: EnumField;
\tstring_field: string| null;
}

''')
