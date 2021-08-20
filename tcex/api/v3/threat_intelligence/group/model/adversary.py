"""Artifact Model"""
# standard library
from tcex.api.v3.threat_intelligence.group.model.group_abc import Groups as GroupsModel
from tcex.api.v3.threat_intelligence.group.model.group_abc import Group as GroupModel


class Adversaries(
    GroupsModel,
    title='Adversaries Model',
):
    pass


class Adversary(
    GroupModel,
    title='Adversary Model',
):
    pass