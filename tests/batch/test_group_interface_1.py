"""Test the TcEx Batch Module."""
# third-party
import pytest


# pylint: disable=no-self-use
class TestGroup1:
    """Test the TcEx Batch Module."""

    def setup_class(self):
        """Configure setup before all tests."""

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-adversary-i1-001', 'Example #1', 'PYTEST1', 'PyTest1'),
            ('pytest-adversary-i1-002', 'Example #2', 'PYTEST2', 'PyTest2'),
            ('pytest-adversary-i1-003', 'Example #3', 'PYTEST3', 'PyTest3'),
            ('pytest-adversary-i1-004', 'Example #4', 'PYTEST4', 'PyTest4'),
        ],
    )
    def test_adversary(self, name, description, label, tag, tcex):
        """Test adversary creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'adversary', name])
        ti = batch.adversary(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-attack-pattern-i1-001', 'Example #1', 'PYTEST1', 'PyTest1'),
            ('pytest-attack-pattern-i1-002', 'Example #2', 'PYTEST2', 'PyTest2'),
            ('pytest-attack-pattern-i1-003', 'Example #3', 'PYTEST3', 'PyTest3'),
            ('pytest-attack-pattern-i1-004', 'Example #4', 'PYTEST4', 'PyTest4'),
        ],
    )
    def test_attack_pattern(self, name, description, label, tag, tcex):
        """Test attack pattern creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'attack_pattern', name])
        ti = batch.attack_pattern(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-campaign-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-campaign-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-campaign-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-campaign-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_campaign(self, name, description, label, tag, tcex):
        """Test campaign creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'campaign', name])
        ti = batch.campaign(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-course-of-action-i1-001', 'Example #1', 'PYTEST1', 'PyTest1'),
            ('pytest-course-of-action-i1-002', 'Example #2', 'PYTEST2', 'PyTest2'),
            ('pytest-course-of-action-i1-003', 'Example #3', 'PYTEST3', 'PyTest3'),
            ('pytest-course-of-action-i1-004', 'Example #4', 'PYTEST4', 'PyTest4'),
        ],
    )
    def test_course_of_action(self, name, description, label, tag, tcex):
        """Test course of action creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'course_of_action', name])
        ti = batch.course_of_action(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-document-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-document-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-document-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-document-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_document(self, name, description, label, tag, tcex):
        """Test document creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'document', name])
        ti = batch.document(name=name, file_name='example.txt', xid=xid)
        ti.file_content = 'Example file content'
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-document-malware-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-document-malware-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-document-malware-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-document-malware-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_document_malware(self, name, description, label, tag, tcex):
        """Test document creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'document', name])
        ti = batch.document(name=name, file_name='example.zip', xid=xid)
        ti.malware = True
        ti.password = 'test'
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-email-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-email-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-email-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-email-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_email(self, name, description, label, tag, tcex):
        """Test email creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'email', name])
        ti = batch.email(
            name=name, subject='subject', header='test', body='this is just a test', xid=xid
        )
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-event-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-event-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-event-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-event-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_event(self, name, description, label, tag, tcex):
        """Test event creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'event', name])
        ti = batch.event(name=name, event_data='2008-12-12T12:12:12Z', xid=xid)
        ti.status = 'Escalated'
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-incident-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-incident-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-incident-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-incident-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_incident(self, name, description, label, tag, tcex):
        """Test incident creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'incident', name])
        ti = batch.incident(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-intrusion_set-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-intrusion_set-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-intrusion_set-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-intrusion_set-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_intrusion_set(self, name, description, label, tag, tcex):
        """Test intrusion_set creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'intrusion_set', name])
        ti = batch.intrusion_set(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-malware-i1-001', 'Example #1', 'PYTEST1', 'PyTest1'),
            ('pytest-malware-i1-002', 'Example #2', 'PYTEST2', 'PyTest2'),
            ('pytest-malware-i1-003', 'Example #3', 'PYTEST3', 'PyTest3'),
            ('pytest-malware-i1-004', 'Example #4', 'PYTEST4', 'PyTest4'),
        ],
    )
    def test_malware(self, name, description, label, tag, tcex):
        """Test malware creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'malware', name])
        ti = batch.malware(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-report-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-report-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-report-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-report-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_report(self, name, description, label, tag, tcex):
        """Test report creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'report', name])
        ti = batch.report(name=name, file_name='report.pdf', publish_date='12-12-2008', xid=xid)
        ti.file_content = 'test 123'
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-signature-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-signature-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-signature-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-signature-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_signature(self, name, description, label, tag, tcex):
        """Test signature creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'signature', name])
        ti = batch.signature(
            name=name, file_name='test.snort', file_type='snort', file_text='test', xid=xid
        )
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-tactic-i1-001', 'Example #1', 'PYTEST1', 'PyTest1'),
            ('pytest-tactic-i1-002', 'Example #2', 'PYTEST2', 'PyTest2'),
            ('pytest-tactic-i1-003', 'Example #3', 'PYTEST3', 'PyTest3'),
            ('pytest-tactic-i1-004', 'Example #4', 'PYTEST4', 'PyTest4'),
        ],
    )
    def test_tactic(self, name, description, label, tag, tcex):
        """Test tactic creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'tactic', name])
        ti = batch.tactic(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-threat-i1-001', 'Example #1', 'PYTEST:1', 'PyTest1'),
            ('pytest-threat-i1-002', 'Example #2', 'PYTEST:2', 'PyTest2'),
            ('pytest-threat-i1-003', 'Example #3', 'PYTEST:3', 'PyTest3'),
            ('pytest-threat-i1-004', 'Example #4', 'PYTEST:4', 'PyTest4'),
        ],
    )
    def test_threat(self, name, description, label, tag, tcex):
        """Test threat creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'threat', name])
        ti = batch.threat(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-tool-i1-001', 'Example #1', 'PYTEST1', 'PyTest1'),
            ('pytest-tool-i1-002', 'Example #2', 'PYTEST2', 'PyTest2'),
            ('pytest-tool-i1-003', 'Example #3', 'PYTEST3', 'PyTest3'),
            ('pytest-tool-i1-004', 'Example #4', 'PYTEST4', 'PyTest4'),
        ],
    )
    def test_tool(self, name, description, label, tag, tcex):
        """Test tool creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'tool', name])
        ti = batch.tool(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1

    @pytest.mark.parametrize(
        'name,description,label,tag',
        [
            ('pytest-vulnerability-i1-001', 'Example #1', 'PYTEST1', 'PyTest1'),
            ('pytest-vulnerability-i1-002', 'Example #2', 'PYTEST2', 'PyTest2'),
            ('pytest-vulnerability-i1-003', 'Example #3', 'PYTEST3', 'PyTest3'),
            ('pytest-vulnerability-i1-004', 'Example #4', 'PYTEST4', 'PyTest4'),
        ],
    )
    def test_vulnerability(self, name, description, label, tag, tcex):
        """Test vulnerability creation"""
        batch = tcex.batch(owner='TCI')
        xid = batch.generate_xid(['pytest', 'vulnerability', name])
        ti = batch.vulnerability(name=name, xid=xid)
        ti.attribute(attr_type='Description', attr_value=description, displayed=True)
        ti.security_label(name=label, description='Pytest Label Description', color='ffc0cb')
        ti.tag(name=tag)
        batch.save(ti)
        batch_status = batch.submit_all()
        assert batch_status[0].get('status') == 'Completed'
        assert batch_status[0].get('successCount') == 1
