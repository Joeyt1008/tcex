"""StringArray Types"""
# standard library
from typing import Any

from .array_abc import AbstractArray


class StringArray(AbstractArray):
    """StringArray Field Type"""

    __input_type__ = 'String'
    __playbook_data_type__ = ['String', 'StringArray']
    _split_on = None
    _strip_on_split = False

    @classmethod
    def is_empty_member(cls, value: Any) -> bool:
        """Implement abstract method in Array parent class.

        An empty member of StringArray is ''
        """
        cls.assert_is_member(value)
        return value == ''

    @classmethod
    def is_array_member(cls, value: Any) -> bool:
        """Implement abstract method in Array parent class.

        A member of StringArray is a string instance or None
        """
        return isinstance(value, (str, type(None)))

    @classmethod
    def pre_validation_processor(cls, value: Any) -> Any:
        """Perform splitting of String values depending on value of _split_on"""

        # cannot use is_empty_member, is_null_member as value can be a list, which would
        # result in an exception
        if isinstance(value, str) and value != '' and cls._split_on is not None:
            if cls._strip_on_split:
                return [val.strip() for val in value.split(cls._split_on) if val.strip()]

            return value.split(cls._split_on)

        return value


class StringArrayOptional(StringArray):
    """StringArrayOptional Field Type"""

    _optional = True