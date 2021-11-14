"""Workflow_Template / Workflow_Templates Model"""
# pylint: disable=no-member,no-self-argument,no-self-use,wrong-import-position
# standard library
from datetime import datetime
from typing import List, Optional

# third-party
from pydantic import BaseModel, Extra, Field, validator

# first-party
from tcex.api.tc.v3.v3_model_abc import V3ModelABC
from tcex.utils import Utils

# json-encoder
json_encoders = {datetime: lambda v: v.isoformat()}


class WorkflowTemplatesModel(
    BaseModel,
    title='WorkflowTemplates Model',
    alias_generator=Utils().snake_to_camel,
    validate_assignment=True,
):
    """Workflow_Templates Model"""

    data: Optional[List['WorkflowTemplateModel']] = Field(
        [],
        description='The data for the WorkflowTemplates.',
        methods=['POST', 'PUT'],
        title='data',
    )
    mode: str = Field(
        'append',
        description='The PUT mode for nested objects (append, delete, replace). Default: append',
        methods=['POST', 'PUT'],
        title='append',
    )


class WorkflowTemplateDataModel(
    BaseModel,
    title='WorkflowTemplate Data Model',
    alias_generator=Utils().snake_to_camel,
    validate_assignment=True,
):
    """Workflow_Templates Data Model"""

    data: Optional[List['WorkflowTemplateModel']] = Field(
        [],
        description='The data for the WorkflowTemplates.',
        methods=['POST', 'PUT'],
        title='data',
    )


class WorkflowTemplateModel(
    V3ModelABC,
    alias_generator=Utils().snake_to_camel,
    extra=Extra.allow,
    title='WorkflowTemplate Model',
    validate_assignment=True,
    json_encoders=json_encoders,
):
    """Workflow_Template Model"""

    active: bool = Field(
        None,
        allow_mutation=False,
        description='The **active** for the Workflow_Template.',
        read_only=True,
        title='active',
    )
    assignee: Optional['AssigneeModel'] = Field(
        None,
        allow_mutation=False,
        description='The **assignee** for the Workflow_Template.',
        read_only=True,
        title='assignee',
    )
    cases: Optional['CasesModel'] = Field(
        None,
        allow_mutation=False,
        description='The **cases** for the Workflow_Template.',
        read_only=True,
        title='cases',
    )
    config_artifact: Optional[str] = Field(
        None,
        allow_mutation=False,
        description='The **config artifact** for the Workflow_Template.',
        read_only=True,
        title='configArtifact',
    )
    config_attribute: Optional[dict] = Field(
        None,
        description='The **config attribute** for the Workflow_Template.',
        methods=['POST', 'PUT'],
        read_only=False,
        title='configAttribute',
    )
    config_playbook: Optional[str] = Field(
        None,
        allow_mutation=False,
        description='The **config playbook** for the Workflow_Template.',
        read_only=True,
        title='configPlaybook',
    )
    config_task: Optional[dict] = Field(
        None,
        allow_mutation=False,
        description='The **config task** for the Workflow_Template.',
        read_only=True,
        title='configTask',
    )
    description: Optional[str] = Field(
        None,
        description='The **description** for the Workflow_Template.',
        methods=['POST', 'PUT'],
        max_length=1500,
        min_length=0,
        read_only=False,
        title='description',
    )
    id: Optional[int] = Field(
        None,
        description='The ID of the item.',
        read_only=True,
        title='id',
    )
    name: Optional[str] = Field(
        None,
        description='The **name** for the Workflow_Template.',
        methods=['POST', 'PUT'],
        max_length=255,
        min_length=1,
        read_only=False,
        title='name',
    )
    version: Optional[int] = Field(
        None,
        description='The **version** for the Workflow_Template.',
        methods=['POST', 'PUT'],
        minimum=1,
        read_only=False,
        title='version',
    )

    @validator('assignee', always=True)
    def _validate_assignee(cls, v):
        if not v:
            return AssigneeModel()
        return v

    @validator('cases', always=True)
    def _validate_cases(cls, v):
        if not v:
            return CasesModel()
        return v


# first-party
from tcex.api.tc.v3.cases.case_model import CasesModel
from tcex.api.tc.v3.security.assignee import AssigneeModel  # pylint: disable=unused-import

# add forward references
WorkflowTemplateDataModel.update_forward_refs()
WorkflowTemplateModel.update_forward_refs()
WorkflowTemplatesModel.update_forward_refs()
