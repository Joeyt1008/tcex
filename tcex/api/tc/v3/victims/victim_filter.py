"""Victim TQL Filter"""
# standard library
from enum import Enum

# first-party
from tcex.api.tc.v3.api_endpoints import ApiEndpoints
from tcex.api.tc.v3.filter_abc import FilterABC
from tcex.api.tc.v3.tql.tql import Tql
from tcex.api.tc.v3.tql.tql_operator import TqlOperator
from tcex.api.tc.v3.tql.tql_type import TqlType


class VictimFilter(FilterABC):
    """Filter Object for Victims"""

    @property
    def _api_endpoint(self) -> str:
        """Return the API endpoint."""
        return ApiEndpoints.VICTIMS.value

    def asset_name(self, operator: Enum, asset_name: str) -> None:
        """Filter Asset Name based on **assetName** keyword.

        Args:
            operator: The operator enum for the filter.
            asset_name: The asset name assigned to a victim.
        """
        self._tql.add_filter('assetName', operator, asset_name, TqlType.STRING)

    def asset_type(self, operator: Enum, asset_type: int) -> None:
        """Filter Asset Type ID based on **assetType** keyword.

        Args:
            operator: The operator enum for the filter.
            asset_type: The asset type ID assigned to a victim.
        """
        self._tql.add_filter('assetType', operator, asset_type, TqlType.INTEGER)

    def asset_typename(self, operator: Enum, asset_typename: str) -> None:
        """Filter Asset Type Name based on **assetTypename** keyword.

        Args:
            operator: The operator enum for the filter.
            asset_typename: The asset type name assigned to a victim.
        """
        self._tql.add_filter('assetTypename', operator, asset_typename, TqlType.STRING)

    def attribute(self, operator: Enum, attribute: str) -> None:
        """Filter attribute based on **attribute** keyword.

        Args:
            operator: The operator enum for the filter.
            attribute: No description provided.
        """
        self._tql.add_filter('attribute', operator, attribute, TqlType.STRING)

    def description(self, operator: Enum, description: str) -> None:
        """Filter Description based on **description** keyword.

        Args:
            operator: The operator enum for the filter.
            description: The description of the victim.
        """
        self._tql.add_filter('description', operator, description, TqlType.STRING)

    def has_attribute(self, operator: Enum, has_attribute: int) -> None:
        """Filter Associated Attribute based on **hasAttribute** keyword.

        Args:
            operator: The operator enum for the filter.
            has_attribute: A nested query for association to other attributes.
        """
        self._tql.add_filter('hasAttribute', operator, has_attribute, TqlType.INTEGER)

    @property
    def has_group(self):
        """Return **GroupFilter** for further filtering."""
        # first-party
        from tcex.api.tc.v3.groups.group_filter import GroupFilter

        groups = GroupFilter(Tql())
        self._tql.add_filter('hasGroup', TqlOperator.EQ, groups, TqlType.SUB_QUERY)
        return groups

    @property
    def has_indicator(self):
        """Return **IndicatorFilter** for further filtering."""
        # first-party
        from tcex.api.tc.v3.indicators.indicator_filter import IndicatorFilter

        indicators = IndicatorFilter(Tql())
        self._tql.add_filter('hasIndicator', TqlOperator.EQ, indicators, TqlType.SUB_QUERY)
        return indicators

    def has_security_label(self, operator: Enum, has_security_label: int) -> None:
        """Filter Associated Security Label based on **hasSecurityLabel** keyword.

        Args:
            operator: The operator enum for the filter.
            has_security_label: A nested query for association to other security labels.
        """
        self._tql.add_filter('hasSecurityLabel', operator, has_security_label, TqlType.INTEGER)

    @property
    def has_tag(self):
        """Return **TagFilter** for further filtering."""
        # first-party
        from tcex.api.tc.v3.tags.tag_filter import TagFilter

        tags = TagFilter(Tql())
        self._tql.add_filter('hasTag', TqlOperator.EQ, tags, TqlType.SUB_QUERY)
        return tags

    def has_victim(self, operator: Enum, has_victim: int) -> None:
        """Filter Associated Victim based on **hasVictim** keyword.

        Args:
            operator: The operator enum for the filter.
            has_victim: A nested query for association to other victims.
        """
        self._tql.add_filter('hasVictim', operator, has_victim, TqlType.INTEGER)

    def has_victim_asset(self, operator: Enum, has_victim_asset: int) -> None:
        """Filter Associated Victim Asset based on **hasVictimAsset** keyword.

        Args:
            operator: The operator enum for the filter.
            has_victim_asset: A nested query for association to other victim assets.
        """
        self._tql.add_filter('hasVictimAsset', operator, has_victim_asset, TqlType.INTEGER)

    def id(self, operator: Enum, id: int) -> None:  # pylint: disable=redefined-builtin
        """Filter ID based on **id** keyword.

        Args:
            operator: The operator enum for the filter.
            id: The ID of the victim.
        """
        self._tql.add_filter('id', operator, id, TqlType.INTEGER)

    def name(self, operator: Enum, name: str) -> None:
        """Filter Name based on **name** keyword.

        Args:
            operator: The operator enum for the filter.
            name: The name of the victim.
        """
        self._tql.add_filter('name', operator, name, TqlType.STRING)

    def nationality(self, operator: Enum, nationality: str) -> None:
        """Filter Nationality based on **nationality** keyword.

        Args:
            operator: The operator enum for the filter.
            nationality: The nationality of the victim.
        """
        self._tql.add_filter('nationality', operator, nationality, TqlType.STRING)

    def organization(self, operator: Enum, organization: str) -> None:
        """Filter Organization based on **organization** keyword.

        Args:
            operator: The operator enum for the filter.
            organization: The organization of the victim.
        """
        self._tql.add_filter('organization', operator, organization, TqlType.STRING)

    def owner(self, operator: Enum, owner: int) -> None:
        """Filter Owner ID based on **owner** keyword.

        Args:
            operator: The operator enum for the filter.
            owner: The owner ID of the victim.
        """
        self._tql.add_filter('owner', operator, owner, TqlType.INTEGER)

    def owner_name(self, operator: Enum, owner_name: str) -> None:
        """Filter Owner Name based on **ownerName** keyword.

        Args:
            operator: The operator enum for the filter.
            owner_name: The owner name of the victim.
        """
        self._tql.add_filter('ownerName', operator, owner_name, TqlType.STRING)

    def security_label(self, operator: Enum, security_label: str) -> None:
        """Filter Security Label based on **securityLabel** keyword.

        Args:
            operator: The operator enum for the filter.
            security_label: The name of a security label applied to the victim.
        """
        self._tql.add_filter('securityLabel', operator, security_label, TqlType.STRING)

    def sub_org(self, operator: Enum, sub_org: str) -> None:
        """Filter Sub-organization based on **subOrg** keyword.

        Args:
            operator: The operator enum for the filter.
            sub_org: The sub-organization of the victim.
        """
        self._tql.add_filter('subOrg', operator, sub_org, TqlType.STRING)

    def summary(self, operator: Enum, summary: str) -> None:
        """Filter Summary based on **summary** keyword.

        Args:
            operator: The operator enum for the filter.
            summary: The name of the victim.
        """
        self._tql.add_filter('summary', operator, summary, TqlType.STRING)

    def tag(self, operator: Enum, tag: str) -> None:
        """Filter Tag based on **tag** keyword.

        Args:
            operator: The operator enum for the filter.
            tag: The name of a tag applied to the victim.
        """
        self._tql.add_filter('tag', operator, tag, TqlType.STRING)

    def tag_owner(self, operator: Enum, tag_owner: int) -> None:
        """Filter Tag Owner ID based on **tagOwner** keyword.

        Args:
            operator: The operator enum for the filter.
            tag_owner: The owner ID of a tag applied to the victim.
        """
        self._tql.add_filter('tagOwner', operator, tag_owner, TqlType.INTEGER)

    def tag_owner_name(self, operator: Enum, tag_owner_name: str) -> None:
        """Filter Tag Owner Name based on **tagOwnerName** keyword.

        Args:
            operator: The operator enum for the filter.
            tag_owner_name: The owner name of a tag applied to the victim.
        """
        self._tql.add_filter('tagOwnerName', operator, tag_owner_name, TqlType.STRING)

    def work_location(self, operator: Enum, work_location: str) -> None:
        """Filter Work Location based on **workLocation** keyword.

        Args:
            operator: The operator enum for the filter.
            work_location: The work location of the victim.
        """
        self._tql.add_filter('workLocation', operator, work_location, TqlType.STRING)