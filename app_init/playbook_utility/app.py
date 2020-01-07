# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""
import json

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


# pylint: disable=W0201
class App(PlaybookApp):
    """Playbook App"""

    def __init__(self, _tcex):
        """Initialize class properties.

        This method can be OPTIONALLY overridden.
        """
        super().__init__(_tcex)
        self.pretty_json = {}

    # def done(self):
    #     """Perform cleanup work before after App main logic."""
    #     self.tcex.log.debug('Running done.')

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        # read inputs
        indent = int(self.tcex.playbook.read(self.args.indent))
        json_data = self.tcex.playbook.read(self.args.json_data)

        # get the playbook variable type
        json_data_type = self.tcex.playbook.variable_type(self.args.json_data)

        # convert string input to dict
        if json_data_type in ['String']:
            json_data = json.loads(json_data)

        # generate the new "pretty" json (this will be used as an option variable)
        try:
            self.pretty_json = json.dumps(json_data, indent=indent, sort_keys=self.args.sort_keys)
        except Exception:
            self.tcex.exit(1, 'Failed parsing JSON data.')

        # set the App exit message
        self.exit_message = 'JSON prettified.'

    # def start(self):
    #     """Perform prep work before running App main logic."""
    #     self.tcex.log.debug('Running start.')

    def write_output(self):
        """Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.
        """
        self.tcex.log.info('Writing Output')
        self.tcex.playbook.create_output('json.pretty', self.pretty_json)