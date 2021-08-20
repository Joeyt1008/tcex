"""Test the TcEx Batch Module."""
# standard library
import os
from datetime import datetime, timedelta


class TestAttributes:
    """Test the TcEx Batch Module."""

    @staticmethod
    def test_adversary(request, tcex):
        """Test batch attributes creation"""
        adversary = tcex.api.v3.ti.group.adversary(name='v3 adversary')
        response = adversary.submit()
        print(response)
        print(adversary)

