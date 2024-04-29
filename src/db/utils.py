
from sqlite3 import Cursor
from typing import Any, Callable, Tuple, Type, TypeVar, cast
from functools import wraps


class NotFoundError(Exception):
    pass


class NotCreatedError(Exception):
    pass

# Generoitu koodi alkaa


T = TypeVar('T')


def require_id(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, obj: Any, *args, **kwargs) -> T:
        # Check for an 'id' attribute in the object
        if not hasattr(obj, 'id') or getattr(obj, 'id') is None:
            raise ValueError("Object must have a non-null 'id' attribute")
        return func(self, obj, *args, **kwargs)
    return cast(Callable[..., T], wrapper)

# Generoitu koodi loppuu


E = TypeVar('E')


def map_result_to_entity(entity_class: Type[E], result: "Tuple[Any]", cursor_description) -> E:
    """
    Map a result from a database query to a entity object.
    Ensure that the column names in the database match the attribute names of the User class.

    :param entity_class: A class object representing the entity.
    :param result: A result from a database query.
    :param cur: A database cursor object.
    :return: A User object.
    """
    column_names = [desc[0] for desc in cursor_description]
    entity_data = dict(zip(column_names, result))
    return entity_class(**entity_data)
