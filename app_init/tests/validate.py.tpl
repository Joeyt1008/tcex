# -*- coding: utf-8 -*-
"""Validate App outputs Class."""
# flake8: noqa
# pylint: disable=line-too-long


class Validate(object):
    """Validate base class for App output validation."""

    def __init__(self, validator):
        """Initialize class properties."""
        self.validator = validator
        self.validation_methods = {
            % for data in output_data:
            '${data['variable']}': self.${data['method']},
            % endfor
        }

    def validate(self, output_variables):
        """Validate Redis output data."""
        if output_variables is None:
            return

        for k, v in output_variables.items():
            method = self.validation_methods.get(k)
            if method is not None:
                method(dict(v))
            else:
                assert False, f'Unknown output variable found in profile: {k}'
    % for data in output_data:
    def ${data['method']}(self, data):
        """Assert for ${data['variable']}."""
        output_var = '${data['variable']}'
        passed, assert_error = self.validator.redis.data(
            output_var, data.pop('expected_output'), data.pop('op', '='), **data
        )
        assert passed, assert_error
    % endfor
