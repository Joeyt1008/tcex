"""Group_Attribute / Group_Attributes Model"""
# pylint: disable=no-member,no-self-argument,no-self-use,wrong-import-position
# standard library
from datetime import datetime
from typing import List, Optional

# third-party
from pydantic import BaseModel, Extra, Field, validator

# first-party
from tcex.utils import Utils


class GroupAttributesModel(
    BaseModel,
    title='GroupAttributes Model',
    alias_generator=Utils().snake_to_camel,
    validate_assignment=True,
):
    """Group_Attributes Model"""

    data: Optional[List['GroupAttributeModel']] = Field(
        [],
        description='The data for the GroupAttributes.',
        methods=['POST', 'PUT'],
        title='data',
    )


class GroupAttributeDataModel(
    BaseModel,
    title='GroupAttribute Data Model',
    alias_generator=Utils().snake_to_camel,
    validate_assignment=True,
):
    """Group_Attributes Data Model"""

    data: Optional[List['GroupAttributeModel']] = Field(
        [],
        description='The data for the GroupAttributes.',
        methods=['POST', 'PUT'],
        title='data',
    )


class GroupAttributeModel(
    BaseModel,
    alias_generator=Utils().snake_to_camel,
    extra=Extra.allow,
    title='GroupAttribute Model',
    validate_assignment=True,
):
    """Group_Attribute Model"""

    # slot attributes are not added to dict()/json()
    __slot__ = ('_privates_',)

    def __init__(self, **kwargs):
        """Initialize class properties."""
        super().__init__(**kwargs)
        super().__setattr__('_privates_', {'_modified_': 0})

    def __setattr__(self, name, value):
        """Update modified property on any update."""
        super().__setattr__('_privates_', {'_modified_': self.privates.get('_modified_', 0) + 1})
        super().__setattr__(name, value)

    @property
    def modified(self):
        """Return int value of modified (> 0 means modified)."""
        return self._privates_.get('_modified_', 0)

    @property
    def privates(self):
        """Return privates dict."""
        return self._privates_

    created_by: Optional['UserModel'] = Field(
        None,
        allow_mutation=False,
        description='The **created by** for the Group_Attribute.',
        read_only=True,
        title='createdBy',
    )
    date_added: Optional[datetime] = Field(
        None,
        allow_mutation=False,
        description='The date and time that the Attribute was first created.',
        read_only=True,
        title='dateAdded',
    )
    default: bool = Field(
        None,
        description=(
            'A flag indicating that this is the default attribute of its type within the object. '
            'Only applies to certain attribute and data types.'
        ),
        methods=['POST', 'PUT'],
        read_only=False,
        title='default',
    )
    group_id: Optional[int] = Field(
        None,
        description='Group associated with attribute.',
        methods=['POST'],
        read_only=False,
        title='groupId',
        updatable=False,
    )
    id: Optional[int] = Field(
        None,
        description='The ID of the item.',
        read_only=True,
        title='id',
    )
    last_modified: Optional[datetime] = Field(
        None,
        allow_mutation=False,
        description='The date and time that the Attribute was last modified.',
        read_only=True,
        title='lastModified',
    )
    source: Optional[str] = Field(
        None,
        description='The attribute source.',
        methods=['POST', 'PUT'],
        read_only=False,
        title='source',
    )
    type: Optional[str] = Field(
        None,
        description='The attribute type.',
        methods=['POST'],
        read_only=False,
        title='type',
        updatable=False,
    )
    value: Optional[str] = Field(
        None,
        description='Attribute value.',
        methods=['POST', 'PUT'],
        min_length=1,
        read_only=False,
        title='value',
    )

    @validator('created_by', always=True)
    def _validate_created_by(cls, v):
        if not v:
            return UserModel()
        return v


# first-party
from tcex.api.tc.v3.security.users.user_model import UserModel

# add forward references
GroupAttributeDataModel.update_forward_refs()
GroupAttributeModel.update_forward_refs()
GroupAttributesModel.update_forward_refs()
