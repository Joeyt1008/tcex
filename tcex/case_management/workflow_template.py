# -*- coding: utf-8 -*-
"""ThreatConnect Workflow Template"""
from .api_endpoints import ApiEndpoints
from .common_case_management import CommonCaseManagement
from .common_case_management_collection import CommonCaseManagementCollection
from .filter import Filter
from .tql import TQL


class WorkflowTemplates(CommonCaseManagementCollection):
    """Workflow Template Class for Case Management Collection

    Args:
        tcex (TcEx): An instantiated instance of TcEx object.
        initial_response (dict, optional): Initial data in
            Case Object for Workflow Template. Defaults to None.
        tql_filters (list, optional): List of TQL filters. Defaults to None.
    """

    def __init__(self, tcex, initial_response=None, tql_filters=None):
        """Initialize Class properties"""
        super().__init__(
            tcex,
            ApiEndpoints.WORKFLOW_TEMPLATES,
            initial_response=initial_response,
            tql_filters=tql_filters,
        )

    def __iter__(self):
        """Iterate on Workflow Templates"""
        return self.iterate(initial_response=self.initial_response)

    def entity_map(self, entity):
        """Map a dict to a Workflow Template.

        Args:
            entity (dict): The Workflow Template data.

        Returns:
            CaseManagement.WorkflowTemplate: An Workflow Template Object
        """
        return WorkflowTemplate(self.tcex, **entity)

    @property
    def filter(self):
        """Return instance of FilterWorkflowTemplate Object."""
        return FilterWorkflowTemplates(ApiEndpoints.WORKFLOW_TEMPLATES, self.tcex, self.tql)


class WorkflowTemplate(CommonCaseManagement):
    """WorkflowTemplate object for Case Management.

    Args:
        tcex (TcEx): An instantiated instance of TcEx object.
        active (bool, kwargs): [Read-Only] The **Active** flag for the Workflow Template.
        assigned_group (UserGroup, kwargs): [Read-Only] The **Assigned Group** for the Workflow
            Template.
        assigned_user (User, kwargs): [Read-Only] The **Assigned User** for the Workflow Template.
        assignee (Assignee, kwargs): [Read-Only] The **Assignee** for the Workflow Template.
        cases (Case, kwargs): [Required] The **Cases** for the Workflow Template.
        config_artifact (str, kwargs): [Read-Only] The **Config Artifact** for the Workflow
            Template.
        config_playbook (str, kwargs): [Read-Only] The **Config Playbook** for the Workflow
            Template.
        config_task (dict, kwargs): [Read-Only] The **Config Task** for the Workflow Template.
        description (str, kwargs): The **Description** for the Workflow Template.
        name (str, kwargs): [Required] The **Name** for the Workflow Template.
        organization (Organization, kwargs): [Read-Only] The **Organization** for the Workflow
            Template.
        target_type (str, kwargs): [Read-Only] The **Target Type** for the Workflow Template.
        version (int, kwargs): The **Version** for the Workflow Template.
    """

    def __init__(self, tcex, **kwargs):
        """Initialize Class properties."""
        super().__init__(tcex, ApiEndpoints.WORKFLOW_TEMPLATES, kwargs)
        self._active = kwargs.get('active', True)
        self._assigned_group = kwargs.get('assigned_group', None)
        self._assigned_user = kwargs.get('assigned_user', None)
        self._assignee = kwargs.get('assignee', None)
        self._cases = kwargs.get('cases', None)
        self._config_artifact = kwargs.get('config_artifact', None)
        self._config_playbook = kwargs.get('config_playbook', None)
        self._config_task = kwargs.get('config_task', None)
        self._description = kwargs.get('description', None)
        self._name = kwargs.get('name', None)
        self._organization = kwargs.get('organization', None)
        self._target_type = kwargs.get('target_type', None)
        self._version = kwargs.get('version', None)

    @property
    def active(self):
        """Return the parent **Active** flag for the Workflow Template."""
        return self._active

    @active.setter
    def active(self, active):
        """Set the parent **Active** flag for the Workflow Template."""
        self._active = active

    @property
    def assigned_group(self):
        """Return the parent **Assigned Group** flag for the Workflow Template."""
        return self._assigned_group

    @assigned_group.setter
    def assigned_group(self, assigned_group):
        """Set the parent **Assigned Group** flag for the Workflow Template."""
        self._assigned_group = assigned_group

    @property
    def assigned_user(self):
        """Return the parent **Assigned User** flag for the Workflow Template."""
        return self._assigned_user

    @assigned_user.setter
    def assigned_user(self, assigned_user):
        """Set the parent **Assigned User** flag for the Workflow Template."""
        self._assigned_user = assigned_user

    @property
    def assignee(self):
        """Return the parent **Assignee** flag for the Workflow Template."""
        return self._assignee

    @assignee.setter
    def assignee(self, assignee):
        """Set the parent **Assignee** flag for the Workflow Template."""
        self._assignee = assignee

    @property
    def available_fields(self):
        """Return the available fields to fetch for an Workflow Template."""
        return ['assignees', 'cases', 'organizations', 'user']

    # TODO: BCS fix this
    @property
    def as_entity(self):
        """Return the entity representation of the Workflow Event."""
        return {}

    @property
    def cases(self):
        """Return the parent **Cases** for the Workflow Template."""
        return self._cases

    @property
    def config_artifact(self):
        """Return the parent **Config Artifact** for the Workflow Template."""
        return self._config_artifact

    @property
    def config_playbook(self):
        """Return the parent **Config Playbook** for the Workflow Template."""
        return self._config_playbook

    @property
    def config_task(self):
        """Return the parent **Config Task** for the Workflow Template."""
        return self._config_task

    @property
    def description(self):
        """Return the parent **Description** for the Workflow Template."""
        return self._description

    @description.setter
    def description(self, description):
        """Set the parent **Description** for the Workflow Template."""
        self._description = description

    def entity_mapper(self, entity):
        """Update current object with provided object properties.

        Args:
            entity (dict): An entity dict used to update the Object.
        """
        new_case = WorkflowTemplate(self.tcex, **entity)
        self.__dict__.update(new_case.__dict__)

    @property
    def name(self):
        """Return the parent **Name** for the Workflow Template."""
        return self._name

    @name.setter
    def name(self, name):
        """Set the parent **Name** for the Workflow Template."""
        self._name = name

    @property
    def organization(self):
        """Return the parent **Organization** for the Workflow Template."""
        return self._organization

    @property
    def target_type(self):
        """Return the parent **Target Type** for the Workflow Template."""
        return True

    @property
    def version(self):
        """Return the parent **Version** for the Workflow Template."""
        return self._version

    @version.setter
    def version(self, version):
        """Set the parent **Version** for the Workflow Template."""
        self._version = version


class FilterWorkflowTemplates(Filter):
    """Filter Object for Workflow Event"""

    def active(self, operator, active):
        """Filter Workflow Templates based on **active** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            active (bool): The active status of this template.
        """
        self._tql.add_filter('active', operator, active, TQL.Type.BOOLEAN)

    def assigned_group_id(self, operator, assigned_group_id):
        """Filter Workflow Templates based on **assignedgroupid** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            assigned_group_id (int): The ID of the Group assigned to this template.
        """
        self._tql.add_filter('assignedgroupid', operator, assigned_group_id, TQL.Type.INTEGER)

    def assigned_user_id(self, operator, assigned_user_id):
        """Filter Workflow Templates based on **assigneduserid** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            assigned_user_id (int): The ID of the User assigned to this template.
        """
        self._tql.add_filter('assigneduserid', operator, assigned_user_id, TQL.Type.INTEGER)

    def config_artifact(self, operator, config_artifact):
        """Filter Workflow Templates based on **configartifact** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            config_artifact (str): The artifact config information.
        """
        self._tql.add_filter('configartifact', operator, config_artifact, TQL.Type.STRING)

    def config_playbook(self, operator, config_playbook):
        """Filter Workflow Templates based on **configplaybook** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            config_playbook (str): The playbook config information.
        """
        self._tql.add_filter('configplaybook', operator, config_playbook, TQL.Type.STRING)

    def config_task(self, operator, config_task):
        """Filter Workflow Templates based on **configtask** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            config_task (str): The task config information.
        """
        self._tql.add_filter('configtask', operator, config_task, TQL.Type.STRING)

    def description(self, operator, description):
        """Filter Workflow Templates based on **description** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            description (str): The description of this template.
        """
        self._tql.add_filter('description', operator, description, TQL.Type.STRING)

    def id(self, operator, id):  # pylint: disable=redefined-builtin
        """Filter Workflow Templates based on **id** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            id (int): The ID of the template.
        """
        self._tql.add_filter('id', operator, id, TQL.Type.INTEGER)

    def name(self, operator, name):
        """Filter Workflow Templates based on **name** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            name (str): The name of this template.
        """
        self._tql.add_filter('name', operator, name, TQL.Type.STRING)

    def organization_id(self, operator, organization_id):
        """Filter Workflow Templates based on **organizationid** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            organization_id (int): The ID of the organization associated with this template.
        """
        self._tql.add_filter('organizationid', operator, organization_id, TQL.Type.INTEGER)

    def target_id(self, operator, target_id):
        """Filter Workflow Templates based on **targetid** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            target_id (int): The ID of the target of this template.
        """
        self._tql.add_filter('targetid', operator, target_id, TQL.Type.INTEGER)

    def target_type(self, operator, target_type):
        """Filter Workflow Templates based on **targettype** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            target_type (str): The target type of this template.
        """
        self._tql.add_filter('targettype', operator, target_type, TQL.Type.STRING)

    def version(self, operator, version):
        """Filter Workflow Templates based on **version** keyword.

        Args:
            operator (enum): The operator enum for the filter.
            version (int): The version of this template.
        """
        self._tql.add_filter('version', operator, version, TQL.Type.INTEGER)
