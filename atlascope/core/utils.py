from typing import Any, Callable

from psycopg2.extensions import AsIs, register_adapter as psycopg2_register_adapter


def register_adapter(cls: type) -> Callable[[Callable[[Any], AsIs]], None]:
    """Decorate registering a psycopg2 adapter for a class.

    This is a convenience function that calls psycopg2's
    ``register_adapter()`` function.
    """

    def wrapper(adapter: Callable[[Any], AsIs]) -> None:
        psycopg2_register_adapter(cls, adapter)

    return wrapper
