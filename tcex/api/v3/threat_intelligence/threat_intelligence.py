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

    # Maybe have something like this so the user doesnt need to drill down and can just pass group_type?
    def group_obj(self, group_type, **kwargs):
        pass
