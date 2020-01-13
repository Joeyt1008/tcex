# -*- coding: utf-8 -*-
"""Test the TcEx Threat Intel Module."""
import os
from tcex.case_management.tql import TQL

from .cm_helpers import CMHelper, TestCaseManagement


class TestCase(TestCaseManagement):
    """Test TcEx CM Case Interface."""

    def setup_method(self):
        """Configure setup before all tests."""
        self.cm_helper = CMHelper('case')
        self.cm = self.cm_helper.cm
        self.tcex = self.cm_helper.tcex

    def teardown_method(self):
        """Configure teardown before all tests."""
        if os.getenv('TEARDOWN_METHOD') is None:
            self.cm_helper.cleanup()

    def test_case_api_options(self):
        """Test filter keywords."""
        super().obj_api_options()

    def test_case_code_gen(self):
        """Generate code and docstring from Options methods.

        This is not truly a test case, but best place to store it for now.
        """
        doc_string, filter_map, filter_class = super().obj_code_gen()
        assert doc_string
        assert filter_map
        assert filter_class

    def test_case_filter_keywords(self):
        """Test filter keywords."""
        super().obj_filter_keywords()

    def test_case_object_properties(self):
        """Test properties."""
        super().obj_properties()

    def test_case_create(self, request):
        """Test Case Creation"""
        case_data = {
            'name': request.node.name,
            'severity': 'Low',
            'status': 'Open',
        }
        case = self.cm.case(**case_data)
        case.submit()

        # retrieve case for asserts
        case = self.cm.case(id=case.id)
        case.get()

        # run assertions on returned data
        assert case.name == case_data.get('name')
        assert case.severity == case_data.get('severity')
        assert case.status == case_data.get('status')

        # cleanup case
        case.delete()

    def test_case_delete(self, request):
        """Test Case Deletion"""
        case = self.cm_helper.create_case()

        cases = self.cm.cases()
        cases.filter.name(TQL.Operator.EQ, request.node.name)
        for case in cases:
            if case.name == request.node.name:
                break
        else:
            # if this hit case was not deleted
            assert False, 'No case was return from TQL filter.'

    def test_case_create_with_metadata(self, request):
        """Test Case Creation"""
        case_data = {
            'name': request.node.name,
            'severity': 'Low',
            'status': 'Open',
        }

        # create case
        case = self.cm.case(**case_data)

        # artifact data
        artifact_data = [
            {'summary': 'asn4455', 'intel_type': 'indicator-ASN', 'type': 'ASN'},
            {'summary': 'asn5544', 'intel_type': 'indicator-ASN', 'type': 'ASN'},
        ]

        # add artifacts
        for artifact in artifact_data:
            case.add_artifact(**artifact)

        # note data
        note_data = [f'A note for pytest test {__name__}']

        # add notes
        for note in note_data:
            case.add_note(text=note)

        # tag data
        tag_data = [{'name': f'{__name__}-1'}, {'name': f'{__name__}-2'}]

        # add tags
        for tag in tag_data:
            case.add_tag(**tag)

        # task data
        task_data = [{'name': 'task-1', 'description': 'task description', 'status': 'Pending'}]

        # add task
        for task in task_data:
            case.add_task(**task)

        # submit case
        case.submit()

        # retrieve case for asserts
        case = self.cm.case(id=case.id)
        case.get(all_available_fields=True)

        # run assertions on returned data
        assert case.id
        assert case.name == request.node.name
        assert case.severity == case_data.get('severity')
        assert case.status == case_data.get('status')

        for artifact in case.artifacts:
            assert artifact.summary in [a.get('summary') for a in artifact_data]
            assert artifact.intel_type == 'indicator-ASN'
            assert artifact.type == 'ASN'

        for tag in case.tags:
            assert tag.name in [t.get('name') for t in tag_data]

        for note in case.notes:
            assert note.text in note_data

        for task in case.tasks:
            assert task.name in [t.get('name') for t in task_data]

        # cleanup case
        case.delete()

    def test_case_get_single_by_id(self, request):
        """Test Case get by ID"""
        # create case
        case = self.cm_helper.create_case()

        # retrieve case for asserts
        case = self.cm.case(id=case.id)
        case.get()

        # run assertions on returned data
        assert case.name == request.node.name

    def test_case_get_many(self, request):
        """Test Case get many"""
        # create cases
        self.cm_helper.create_case(name=f'{request.node.name}-1', xid=f'{request.node.name}-1')
        self.cm_helper.create_case(name=f'{request.node.name}-2', xid=f'{request.node.name}-2')

        # specifically match the count of the cases created.
        case_count = 0
        for case in self.cm.cases():
            if case.name.startswith(request.node.name):
                case_count += 1

        # run assertions on case count
        assert case_count == 2

    # def test_case_get_by_tql_filter_artifact_id(self, request):
    #     """Test Case Get by TQL"""
    #     # create case
    #     case = self.cm_helper.create_case()

    #     # artifact data
    #     artifact_data = {
    #         'case_id': case.id,
    #         'intel_type': 'indicator-ASN',
    #         'summary': f'asn{randint(100, 999)}',
    #         'type': 'ASN',
    #     }

    #     # create artifact
    #     artifact = self.cm.artifact(**artifact_data)
    #     artifact.submit()

    #     # retrieve note using TQL
    #     cases = self.cm.cases()
    #     cases.filter.artifact_id(TQL.Operator.EQ, artifact.id)

    #     for case in cases:
    #         assert case.name == request.node.name
    #         break
    #     else:
    #         assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_created_by(self, request):
        """Test Case Get by TQL"""
        # create case
        case = self.cm_helper.create_case()

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.created_by(TQL.Operator.EQ, os.getenv('API_ACCESS_ID'))

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_created_by_id(self, request):
        """Test Case Get by TQL

        # This method is geared more for the UI as we won't have easy access to user id
        """
        # create case
        case = self.cm_helper.create_case()

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.created_by_id(TQL.Operator.EQ, 5)

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_description(self, request):
        """Test Case Get by TQL"""
        description = f'a test description for {request.node.name}'

        # create case
        case = self.cm_helper.create_case(description=description)

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.description(TQL.Operator.EQ, description)

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    # TODO: this needs some consideration
    def test_case_get_by_tql_filter_hasartifact(self):
        """Test Case Get by TQL"""

    # TODO: this needs some consideration
    def test_case_get_by_tql_filter_hastag(self):
        """Test Case Get by TQL"""

    # TODO: this needs some consideration
    def test_case_get_by_tql_filter_hastask(self):
        """Test Case Get by TQL"""

    def test_case_get_by_tql_filter_id(self, request):
        """Test Case Get by TQL"""
        # create case
        case = self.cm_helper.create_case()

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_owner_name(self, request):
        """Test Case Get by TQL"""
        # create case
        case = self.cm_helper.create_case()

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.owner_name(TQL.Operator.EQ, os.getenv('TC_OWNER'))

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_resolution(self, request):
        """Test Case Get by TQL"""
        resolution = 'Escalated'

        # create case
        case = self.cm_helper.create_case(resolution=resolution)

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.resolution(TQL.Operator.EQ, resolution)

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_severity(self, request):
        """Test Case Get by TQL"""
        severity = 'Low'
        # create case
        case = self.cm_helper.create_case(severity=severity)

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.severity(TQL.Operator.EQ, severity)

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_status(self, request):
        """Test Case Get by TQL"""
        status = 'Closed'
        # create case
        case = self.cm_helper.create_case(status=status)

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.status(TQL.Operator.EQ, status)

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_tag(self, request):
        """Test Case Get by TQL"""
        # create case
        tag_data = {'name': request.node.name}
        case = self.cm_helper.create_case(tags=tag_data)

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.tag(TQL.Operator.EQ, tag_data.get('name'))

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_target_id(self, request):
        """Test Case Get by TQL"""
        # create case
        assignee = self.cm.assignee(type='User', user_name=os.getenv('API_ACCESS_ID'))
        case = self.cm_helper.create_case(assignee=assignee)

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.target_id(TQL.Operator.EQ, 5)

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_target_type(self, request):
        """Test Case Get by TQL"""
        # create case
        assignee = self.cm.assignee(type='User', user_name=os.getenv('API_ACCESS_ID'))
        case = self.cm_helper.create_case(assignee=assignee)

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.target_type(TQL.Operator.EQ, 'User')

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'

    def test_case_get_by_tql_filter_xid(self, request):
        """Test Case Get by TQL"""
        # create case
        xid = request.node.name
        case = self.cm_helper.create_case(xid=xid)

        # retrieve note using TQL
        cases = self.cm.cases()
        cases.filter.id(TQL.Operator.EQ, case.id)
        cases.filter.xid(TQL.Operator.EQ, xid)

        for case in cases:
            assert case.name == request.node.name
            break
        else:
            assert False, 'No cases returned for TQL'
