"""Case Management"""
# third-party
from requests import Session

# first-party
from tcex.api.v3.threat_intelligence.group.group import Group
from tcex.api.v3.threat_intelligence.indicator.indicator import Indicator


class ThreatIntelligence:
    """Case Management

    Args:
        session: An configured instance of request.Session with TC API Auth.
    """

    def __init__(self, session: Session) -> None:
        """Initialize Class properties."""
        self.session = session

    @property
    def group(self) -> Group:
        """Return a instance of Adversary object."""

        return Group(session=self.session)

    @property
    def indicator(self) -> Indicator:
        """Return a instance of Adversary object."""

        return Indicator(session=self.session)

    def get_group(self, group_type):
        self.group.__getattribute__(group_type.lower())

    def get_indicator(self, indicator_type):
        self.group.__getattribute__(indicator_type.lower())
