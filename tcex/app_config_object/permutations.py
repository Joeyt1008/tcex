#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TcEx Framework LayoutJson."""
import json
import os
import sys

import sqlite3

from .install_json import InstallJson
from .layout_json import LayoutJson


class Permutations:
    """Permutations Module"""

    def __init__(self):
        """Initialize Class properties"""
        # self.args = _args

        # properties
        self._db_conn = None
        self._input_permutations = None
        self._output_permutations = None
        # self._redis = None
        # self._tcex_json = None
        self.app_path = os.getcwd()
        # self.exit_code = 0
        self.ij = InstallJson()
        self.lj = LayoutJson()
        self.input_table = 'inputs'
        # self.output = []

    def _gen_permutations(self, index=0, args=None):
        """Iterate recursively over layout.json parameter names to build permutations.

        .. NOTE:: Permutations are for layout.json based Apps.

        Args:
            index (int, optional): The current index position in the layout names list.
            args (list, optional): Defaults to None. The current list of args.
        """
        if args is None:
            args = []
        try:
            hidden = False
            if self.ij.runtime_level.lower() in [
                'playbook',
                'triggerservice',
                'webhooktriggerservice',
            ]:
                name = list(self.lj.parameters_names)[index]
                display = self.lj.parameters_dict.get(name, {}).get('display')
                hidden = self.lj.parameters_dict.get(name, {}).get('hidden', False)
            else:
                name = list(self.ij.params_dict.keys())[index]
                display = False

            input_type = self.ij.params_dict.get(name, {}).get('type')
            if input_type is None:
                self.handle_error(f'No value found in install.json for "{name}".')

            if (
                self.ij.runtime_level.lower() == 'organization'
                or self.validate_layout_display(self.input_table, display)
                or hidden
            ):
                if input_type.lower() == 'boolean':
                    for val in [True, False]:
                        args.append({'name': name, 'value': val})
                        self.db_update_record(self.input_table, name, val)
                        self._gen_permutations(index + 1, list(args))
                        # remove the previous arg before next iteration
                        args.pop()
                elif input_type.lower() == 'choice':
                    valid_values = self.ij.expand_valid_values(
                        self.ij.params_dict.get(name, {}).get('validValues', [])
                    )
                    for val in valid_values:
                        args.append({'name': name, 'value': val})
                        self.db_update_record(self.input_table, name, val)
                        self._gen_permutations(index + 1, list(args))
                        # remove the previous arg before next iteration
                        args.pop()
                else:
                    args.append({'name': name, 'value': None})
                    self._gen_permutations(index + 1, list(args))
            else:
                self._gen_permutations(index + 1, list(args))

        except IndexError:
            # when IndexError is reached all data has been processed.
            self._input_permutations.append(args)
            outputs = []

            for o_name in self.ij.output_variables_dict():
                if self.lj.outputs_dict.get(o_name) is not None:
                    display = self.lj.outputs_dict.get(o_name, {}).get('display')
                    valid = self.validate_layout_display(self.input_table, display)
                    if display is None or not valid:
                        continue
                outputs.append(self.ij.output_variables_dict().get(o_name))
            self._output_permutations.append(outputs)

    @property
    def db_conn(self):
        """Create a temporary in memory DB and return the connection."""
        if self._db_conn is None:
            try:
                self._db_conn = sqlite3.connect(':memory:')
            except sqlite3.Error as e:
                self.handle_error(e)
        return self._db_conn

    def db_create_table(self, table_name, columns):
        """Create a temporary DB table.

        Arguments:
            table_name (str): The name of the table.
            columns (list): List of columns to add to the DB.
        """
        formatted_columns = ''
        for col in set(columns):
            formatted_columns += f""""{col.strip('"').strip("'")}" text, """
        formatted_columns = formatted_columns.strip(', ')

        create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({formatted_columns});'
        try:
            cr = self.db_conn.cursor()
            cr.execute(create_table_sql)
        except sqlite3.Error as e:
            self.handle_error(e)

    def db_drop_table(self, table_name):
        """Drop a DB table.

        Arguments:
            table_name (str): The name of the table.
        """
        create_table_sql = f'DROP TABLE IF EXISTS {table_name};'
        try:
            cr = self.db_conn.cursor()
            cr.execute(create_table_sql)
        except sqlite3.Error as e:
            self.handle_error(e)

    def db_insert_record(self, table_name, columns):
        """Insert records into DB.

        Args:
            table_name (str): The name of the table.
            columns (list): List of columns for insert statement.
        """
        bindings = ('?,' * len(columns)).strip(',')
        values = [None] * len(columns)
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({bindings})"
        cur = self.db_conn.cursor()
        cur.execute(sql, values)

    def db_update_record(self, table_name, column, value):
        """Insert records into DB.

        Args:
            table_name (str): The name of the table.
            column (str): The column name in which the value is to be updated.
            value (str): The value to update in the column.
        """
        sql = f'UPDATE {table_name} SET {column} = \'{value}\''
        cur = self.db_conn.cursor()
        cur.execute(sql)

    @property
    def filename(self):
        """Return all output permutations for current App."""
        return os.path.join(self.app_path, 'permutations.json')

    @staticmethod
    def handle_error(err, halt=True):
        """Print errors message and optionally exit.

        Args:
            err (str): The error message to print.
            halt (bool, optional): Defaults to True. If True the script will exit.
        """
        print(err)
        if halt:
            sys.exit(1)

    def init_permutations(self):
        """Process layout.json names/display to get all permutations of args."""
        if self._input_permutations is None and self._output_permutations is None:
            self._input_permutations = []
            self._output_permutations = []

            # create db for permutations testing
            self.db_create_table(self.input_table, self.ij.params_dict.keys())
            self.db_insert_record(self.input_table, self.ij.params_dict.keys())

            # only gen permutations if none have been generated previously
            self._gen_permutations()

            # drop database
            self.db_drop_table(self.input_table)

    @property
    def input_permutations(self):
        """Return all input permutations for current App."""
        if self._input_permutations is None:
            self.init_permutations()
        return self._input_permutations

    @property
    def output_permutations(self):
        """Return all output permutations for current App."""
        if self._output_permutations is None:
            self.init_permutations()
        return self._output_permutations

    def permutations(self):
        """Process layout.json names/display to get all permutations of args."""
        # if 'sqlite3' not in sys.modules:
        #     print('The sqlite3 module needs to be build-in to Python for this feature.')
        #     sys.exit(1)

        # create db for permutations testing
        self.db_create_table(self.input_table, self.ij.params_dict.keys())
        self.db_insert_record(self.input_table, self.ij.params_dict.keys())

        # only gen permutations if none have been generated previously
        if not self._input_permutations and not self._output_permutations:
            self._gen_permutations()

        # output permutations
        self.write_permutations_file()

    def validate_layout_display(self, table, display_condition):
        """Check to see if the display condition passes.

        Args:
            table (str): The name of the DB table which hold the App data.
            display_condition (str): The "where" clause of the DB SQL statement.

        Returns:
            bool: True if the row count is greater than 0.
        """
        display = False
        if display_condition is None:
            display = True
        else:
            display_query = f'select count(*) from {table} where {display_condition}'
            try:
                cur = self.db_conn.cursor()
                cur.execute(display_query.replace('"', ''))
                rows = cur.fetchall()
                if rows[0][0] > 0:
                    display = True
            except sqlite3.Error as e:
                print(f'"{display_query}" query returned an error: ({e}).')
                sys.exit(1)
        return display

    def write_permutations_file(self):
        """Print all valid permutations."""
        permutations = []
        for p, index in enumerate(self._input_permutations):
            permutations.append({'index': index, 'args': p})

        with open(self.filename, 'w') as fh:
            json.dump(permutations, fh, indent=2, sort_keys=True)
        print('All permutations written to the "permutations.json" file.')
