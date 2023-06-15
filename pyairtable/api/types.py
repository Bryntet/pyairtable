"""
pyAirtable provides a number of type aliases and TypedDicts which are used as inputs
and return values to various pyAirtable methods.
"""
from functools import lru_cache
from typing import Any, Dict, List, Literal, Optional, Type, TypeVar, Union, cast

import pydantic
from typing_extensions import Required, TypeAlias, TypedDict

T = TypeVar("T")

#: An alias for ``str`` used internally for disambiguation.
#: Record IDs for Airtable look like ``"recAdw9EjV90xbZ"``.
RecordId: TypeAlias = str

#: An alias for ``str`` used internally for disambiguation.
#: Airtable returns timestamps as ISO 8601 UTC strings,
#: e.g. ``"2023-05-22T21:24:15.333134Z"``
Timestamp: TypeAlias = str

#: An alias for ``str`` used internally for disambiguation.
#: Field names can be any valid string.
FieldName: TypeAlias = str


class AttachmentDict(TypedDict, total=False):
    """
    A ``dict`` representing an attachment stored in an Attachments field.

    >>> record = table.get('recW8eG2x0ew1Af')
    >>> record['fields']['Attachments']
    [
        {
            'id': 'attW8eG2x0ew1Af',
            'url': 'https://example.com/hello.jpg',
            'filename': 'hello.jpg'
        }
    ]

    See https://airtable.com/developers/web/api/field-model#multipleattachment
    """

    id: Required[str]
    url: Required[str]
    type: str
    filename: str
    size: int
    height: int
    width: int
    thumbnails: Dict[str, Dict[str, Union[str, int]]]


class CreateAttachmentDict(TypedDict, total=False):
    """
    A ``dict`` representing a new attachment to be written to the Airtable API.

    >>> new_attachment = {
    ...     "url": "https://example.com/image.jpg",
    ...     "filename": "something_else.jpg",
    ... }
    >>> existing = record["fields"].setdefault("Attachments", [])
    >>> existing.append(new_attachment)
    >>> table.update(existing["id"], existing["fields"])
    """

    url: Required[str]
    filename: str


class BarcodeDict(TypedDict, total=False):
    """
    A ``dict`` representing the value stored in a Barcode field.

    >>> record = table.get('recW8eG2x0ew1Af')
    >>> record['fields']['Barcode']
    {'type': 'upce', 'text': '01234567'}

    See https://airtable.com/developers/web/api/field-model#barcode
    """

    type: str
    text: Required[str]


class ButtonDict(TypedDict):
    """
    A ``dict`` representing the value stored in a Button field.

    >>> record = table.get('recW8eG2x0ew1Af')
    >>> record['fields']['Click Me']
    {'label': 'Click Me', 'url': 'http://example.com'}

    See https://airtable.com/developers/web/api/field-model#button
    """

    label: str
    url: Optional[str]


class CollaboratorDict(TypedDict, total=False):
    """
    A dict representing the value stored in a User field returned from the API.

    >>> record = table.get('recW8eG2x0ew1Af')
    >>> record['fields']['Created By']
    {
        'id': 'usrAdw9EjV90xbW',
        'email': 'alice@example.com',
        'name': 'Alice Arnold'
    }
    >>> record['fields']['Collaborators']
    [
        {
            'id': 'usrAdw9EjV90xbW',
            'email': 'alice@example.com',
            'name': 'Alice Arnold'
        },
        {
            'id': 'usrAdw9EjV90xbX',
            'email': 'bob@example.com',
            'name': 'Bob Barker'
        }
    ]

    See https://airtable.com/developers/web/api/field-model#collaborator
    """

    id: Required[str]
    email: str
    name: str
    profilePicUrl: str


class CollaboratorEmailDict(TypedDict):
    """
    A dict representing a collaborator identified by email, not by ID.
    Often used when writing to the API, because the email of a collaborator
    may be more easily accessible than their Airtable user ID.

    >>> table = Table("access_token", "base_id", "api_key")
    >>> record = table.update("recW8eG2x0ew1Af", {
    ...     "Collaborator": {"email": "alice@example.com"}
    ... })
    >>> record
    {
        'id': 'recW8eG2x0ew1Af',
        'createdTime': 2023-06-07T17:35:17Z',
        'fields': {
            'Collaborator': {
                'id': 'usrAdw9EjV90xbW',
                'email': 'alice@example.com',
                'name': 'Alice Arnold'
            }
        }
    }
    """

    email: str


class FormulaErrorDict(TypedDict):
    """
    The dict returned by Airtable to indicate a formula error.
    """

    error: str


class FormulaNotANumberDict(TypedDict):
    """
    The dict returned by Airtable to indicate a NaN result.
    """

    specialValue: Literal["NaN"]


#: Represents the types of values that an Airtable field could provide.
#: For more information on Airtable field types, see
#: `Field types and cell values <https://airtable.com/developers/web/api/field-model>`__.
FieldValue: TypeAlias = Union[
    str,
    int,
    float,
    bool,
    CollaboratorDict,
    CollaboratorEmailDict,
    BarcodeDict,
    ButtonDict,
    List[str],
    List[int],
    List[float],
    List[bool],
    List[AttachmentDict],
    List[CollaboratorDict],
    List[CollaboratorEmailDict],
    FormulaErrorDict,
    FormulaNotANumberDict,
]


#: A mapping of field names to values.
Fields: TypeAlias = Dict[FieldName, Optional[FieldValue]]


class RecordDict(TypedDict):
    """
    A ``dict`` representing a record returned from the Airtable API.
    See `List records <https://airtable.com/developers/web/api/list-records>`__.

    Usage:
        >>> table.first(formula="Name = 'Alice'")
        {
            'id': 'recAdw9EjV90xbW',
            'createdTime': '2023-05-22T21:24:15.333134Z',
            'fields': {'Name': 'Alice', 'Department': 'Engineering'}
        }
    """

    id: RecordId
    createdTime: Timestamp
    fields: Fields


class CreateRecordDict(TypedDict):
    """
    A ``dict`` representing the payload passed to the Airtable API to create a record.
    """

    fields: Fields


class UpdateRecordDict(TypedDict):
    """
    A ``dict`` representing the payload passed to the Airtable API to update a record.

    Usage:
        >>> update_records = [
        ...     {"id": "recAdw9EjV90xbW", "fields": {"Email": "alice@example.com"}},
        ...     {"id": "recAdw9EjV90xbX", "fields": {"Email": "bob@example.com"}},
        ... ]
        >>> table.batch_update(update_records)
    """

    id: RecordId
    fields: Fields


class RecordDeletedDict(TypedDict):
    """
    A ``dict`` representing the payload returned by the Airtable API to confirm a deletion.

    Usage:
        >>> table.delete("recAdw9EjV90xbZ")
        {'id': 'recAdw9EjV90xbZ', 'deleted': True}
    """

    id: RecordId
    deleted: bool


@lru_cache
def _create_model_from_typeddict(cls: Type[T]) -> Type[pydantic.BaseModel]:
    """
    Creates a pydantic model from a TypedDict to use as a validator.
    Memoizes the result so we don't have to call this more than once per class.
    """
    return pydantic.create_model_from_typeddict(cls)


def assert_typed_dict(cls: Type[T], obj: Any) -> T:
    """
    Raises a TypeError if the given object is not a dict which conforms
    to the interface declared by the given TypedDict.

    Args:
        cls: The TypedDict class.
        obj: The object that should be a TypedDict.

    Usage:
        >>> assert_typed_dict(
        ...     RecordDict,
        ...     {
        ...         "id": "recAdw9EjV90xbZ",
        ...         "createdTime": "2023-05-22T21:24:15.333134Z",
        ...         "fields": {},
        ...     }
        ... )
        {
            'id': 'recAdw9EjV90xbZ',
            'createdTime': '2023-05-22T21:24:15.333134Z',
            'fields': {}
        }

        >>> assert_typed_dict(RecordDict, {"foo": "bar"})
        Traceback (most recent call last):
        TypeError: dict with keys ['foo'] is not RecordDict
    """
    if not isinstance(obj, dict):
        raise TypeError(f"expected dict, got {type(obj)}")
    # mypy complains cls isn't Hashable, but it is; see https://github.com/python/mypy/issues/2412
    model = _create_model_from_typeddict(cls)  # type: ignore
    try:
        model(**obj)
    except pydantic.ValidationError:
        raise TypeError(f"dict with keys {sorted(obj)} is not {cls.__name__}")
    return cast(T, obj)


def assert_typed_dicts(cls: Type[T], objects: Any) -> List[T]:
    """
    Like :func:`~pyairtable.api.types.assert_typed_dict` but for a list.

    Args:
        cls: The TypedDict class.
        objects: The object that should be a list of TypedDicts.
    """
    if not isinstance(objects, list):
        raise TypeError(f"expected list, got {type(objects)}")
    return [assert_typed_dict(cls, obj) for obj in objects]


def is_airtable_error(obj: Any) -> bool:
    """
    Returns whether the given object represents an Airtable error.
    """
    if isinstance(obj, dict):
        return set(obj) in ({"error"}, {"specialValue"})
    return False