from collections import UserList
import re
from typing import Iterable

from django.db.models import Field, FloatField, Func
from psycopg2.extensions import AsIs

from atlascope.core.utils import register_adapter

__all__ = ['Cube', 'CubeDistance', 'CubeField']


class Cube(UserList):
    data: Iterable[float]


@register_adapter(Cube)
def adapt_cube(cube: Iterable[float]) -> str:
    quoted_vector = [str(x) for x in cube]
    return AsIs("cube(array[%s]::float[])" % ",".join(quoted_vector))


def parse_cube(cube_string: str) -> Cube:
    quoted_vector = re.findall(r'-?\d+(?:\.\d+)?(?:[eE]-?\d+)?', cube_string)
    return Cube([float(s) for s in quoted_vector])


class CubeField(Field):

    description = "An n-d vector using the PostgreSQL cube module"

    def db_type(self, connection):
        return 'cube'

    def from_db_value(self, value, expression, connection):
        if isinstance(value, Cube) or value is None:
            return value
        return parse_cube(value)

    def to_python(self, value):
        if isinstance(value, Cube) or value is None:
            return value
        return parse_cube(value)


class CubeDistance(Func):
    """Computes Euclidean distance between two cubes."""

    template = '%(expressions)s'
    arg_joiner = ' <-> '
    arity = 2

    def __init__(self, *args, **kwargs):
        if kwargs.get('output_field', None) is None:
            kwargs['output_field'] = FloatField()
        super().__init__(*args, **kwargs)
