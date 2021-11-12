"""Artifact / Artifacts Object"""
# standard library
from typing import TYPE_CHECKING

# first-party
from tcex.api.tc.v3.api_endpoints import ApiEndpoints
from tcex.api.tc.v3.artifacts.artifact_filter import ArtifactFilter
from tcex.api.tc.v3.artifacts.artifact_model import ArtifactModel, ArtifactsModel
from tcex.api.tc.v3.notes.note_model import NoteModel
from tcex.api.tc.v3.object_abc import ObjectABC
from tcex.api.tc.v3.object_collection_abc import ObjectCollectionABC
from tcex.api.tc.v3.tql.tql_operator import TqlOperator

if TYPE_CHECKING:  # pragma: no cover
    # first-party
    from tcex.api.tc.v3.notes.note import Note


class Artifacts(ObjectCollectionABC):
    """Artifacts Collection.

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
        self._model = ArtifactsModel(**kwargs)
        self.type_ = 'artifacts'

    def __iter__(self) -> 'Artifact':
        """Iterate over CM objects."""
        return self.iterate(base_class=Artifact)

    @property
    def _api_endpoint(self) -> str:
        """Return the type specific API endpoint."""
        return ApiEndpoints.ARTIFACTS.value

    @property
    def filter(self) -> 'ArtifactFilter':
        """Return the type specific filter object."""
        return ArtifactFilter(self.tql)


class Artifact(ObjectABC):
    """Artifacts Object.

    Args:
        case_id (int, kwargs): The **case id** for the Artifact.
        case_xid (str, kwargs): The **case xid** for the Artifact.
        derived_link (bool, kwargs): Flag to specify if this artifact should be used for potentially
            associated cases or not.
        field_name (str, kwargs): The field name for the artifact.
        file_data (str, kwargs): Base64 encoded file attachment required only for certain artifact
            types.
        hash_code (str, kwargs): Hashcode of Artifact of type File.
        notes (Notes, kwargs): A list of Notes corresponding to the Artifact.
        source (str, kwargs): The **source** for the Artifact.
        summary (str, kwargs): The **summary** for the Artifact.
        task_id (int, kwargs): The ID of the task which the Artifact references.
        task_xid (str, kwargs): The XID of the task which the Artifact references.
        type (str, kwargs): The **type** for the Artifact.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize class properties."""
        super().__init__(kwargs.pop('session', None))
        self._model = ArtifactModel(**kwargs)
        self.type_ = 'Artifact'

    @property
    def _api_endpoint(self) -> str:
        """Return the type specific API endpoint."""
        return ApiEndpoints.ARTIFACTS.value

    @property
    def _base_filter(self) -> dict:
        """Return the default filter."""
        return {
            'keyword': 'artifact_id',
            'operator': TqlOperator.EQ,
            'value': self.model.id,
            'type_': 'integer',
        }

    @property
    def as_entity(self) -> dict:
        """Return the entity representation of the object."""
        type_ = self.type_
        if hasattr(self.model, 'type'):
            type_ = self.model.type

        return {'type': type_, 'id': self.model.id, 'value': self.model.summary}

    def add_note(self, **kwargs) -> None:
        """Add note to the object.

        Args:
            text (str, kwargs): The **text** for the Note.
        """
        self.model.notes.data.append(NoteModel(**kwargs))

    @property
    def notes(self) -> 'Note':
        """Yield Note from Notes."""
        # first-party
        from tcex.api.tc.v3.notes.note import Notes

        yield from self._iterate_over_sublist(Notes)