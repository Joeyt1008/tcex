# -*- coding: utf-8 -*-
"""ThreatConnect TI Signature"""
from tcex.tcex_ti.mappings.group.tcex_ti_group import Group


class Signature(Group):
    """Unique API calls for Signature API Endpoints"""

    def __init__(self, tcex, name, file_name, file_type, file_text, **kwargs):
        """Initialize Class Properties.

        Valid file_types:
        + Snort ®
        + Suricata
        + YARA
        + ClamAV ®
        + OpenIOC
        + CybOX ™
        + Bro
        + Regex
        + SPL - Splunk ® Search Processing Language

        Args:
            name (str): The name for this Group.
            file_name (str): The name for the attached signature for this Group.
            file_type (str): The signature type for this Group.
            file_text (str): The signature content for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
        """
        super(Signature, self).__init__(tcex, 'signatures', name, **kwargs)
        self.api_entity = 'signature'
        self._data['fileName'] = file_name
        self._data['fileType'] = file_type
        self._data['fileText'] = file_text

    def download(self):
        """
        Downloads the signature.

        Returns:

        """
        return self.tc_requests.download(self.api_type, self.api_sub_type, self.unique_id)
