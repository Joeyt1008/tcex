"""Artifact Model"""
# standard library
from typing import Optional, List, Union

# third-party
from pydantic import BaseModel, Extra, Field

# first-party
from tcex.utils import Utils


class Indicators(
    BaseModel,
    title='Indicators Model',
):
    """Artifacts Model"""

    data: 'Optional[List[Indicator]]' = Field(
        [],
        description='The data for the File.',
        title='data',
    )


class Indicator(
    BaseModel,
    title='Indicator Model',
    alias_generator=Utils().snake_to_camel,
    extra=Extra.allow,
    validate_assignment=True
):
    id: Optional[int] = Field(
        None,
        description='The **id** of the Indicator.',
        methods=['POST'],
        id='id',
    )




from tcex.api.v3.threat_intelligence.group.model.adversary import Adversaries

# add forward references
Indicator.update_forward_refs()
Indicators.update_forward_refs()
