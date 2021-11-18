"""AttributeType / AttributeTypes Object"""
# first-party
from tcex.api.tc.v3.api_endpoints import ApiEndpoints
from tcex.api.tc.v3.attribute_types.attribute_type_filter import AttributeTypeFilter
from tcex.api.tc.v3.attribute_types.attribute_type_model import (
    AttributeTypeModel,
    AttributeTypesModel,
)
from tcex.api.tc.v3.object_abc import ObjectABC
from tcex.api.tc.v3.object_collection_abc import ObjectCollectionABC


class AttributeTypes(ObjectCollectionABC):
    """AttributeTypes Collection.

    # Example of params input
    {
        'result_limit': 100,  # Limit the retrieved results.
        'result_start': 10,  # Starting count used for pagination.
        'fields': ['caseId', 'summary']  # Select additional return fields.
    }

    Args:
        session (Session): Session object configured with TC API Auth.
        tql_filters (list): List of TQL filters.
        params (dict): Additional query params (see example above).
    """

    def __init__(self, **kwargs) -> None:
        """Initialize class properties."""
        super().__init__(
            kwargs.pop('session', None), kwargs.pop('tql_filter', None), kwargs.pop('params', None)
        )
        self._model = AttributeTypesModel(**kwargs)
        self.type_ = 'attribute_types'

    def __iter__(self) -> 'AttributeType':
        """Iterate over CM objects."""
        return self.iterate(base_class=AttributeType)

    @property
    def _api_endpoint(self) -> str:
        """Return the type specific API endpoint."""
        return ApiEndpoints.ATTRIBUTE_TYPES.value

    @property
    def filter(self) -> 'AttributeTypeFilter':
        """Return the type specific filter object."""
        return AttributeTypeFilter(self.tql)


class AttributeType(ObjectABC):
    """AttributeTypes Object."""

    def __init__(self, **kwargs) -> None:
        """Initialize class properties."""
        super().__init__(kwargs.pop('session', None))

        # properties
        self._model = AttributeTypeModel(**kwargs)
        self._nested_field_name = 'attributeTypes'
        self._nested_filter = 'has_attribute_type'
        self.type_ = 'Attribute Type'

    @property
    def _api_endpoint(self) -> str:
        """Return the type specific API endpoint."""
        return ApiEndpoints.ATTRIBUTE_TYPES.value