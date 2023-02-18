#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import random

from sos_notebook.test_utils import NotebookTest


class TestDataExchange(NotebookTest):

    def _var_name(self):
        if not hasattr(self, '_var_idx'):
            self._var_idx = 0
        self._var_idx += 1
        return f'var{self._var_idx}'

    def get_from_SoS(self, notebook, sos_expr):
        var_name = self._var_name()
        notebook.call(f'{var_name}={sos_expr}', kernel='SoS')
        return notebook.check_output(
            f'''\
            %get {var_name}
            echo ${var_name}''',
            kernel='Bash')

    def put_to_SoS(self, notebook, bash_expr):
        var_name = self._var_name()
        notebook.call(
            f'''\
            %put {var_name}
            {var_name}={bash_expr}
            ''',
            kernel='Bash')
        return notebook.check_output(f'print(repr({var_name}))', kernel='SoS')

    def test_get_None(self, notebook):
        assert "" == self.get_from_SoS(notebook, 'None')

    def test_get_int(self, notebook):
        assert '123' == self.get_from_SoS(notebook, '123')

    def test_put_int(self, notebook):
        # returns as string
        assert "'123'" == self.put_to_SoS(notebook, '123')

    def test_get_logic(self, notebook):
        assert 'TRUE' == self.get_from_SoS(notebook, 'True')
        assert 'FALSE' == self.get_from_SoS(notebook, 'False')

    def test_get_str(self, notebook):
        assert 'asd' == self.get_from_SoS(notebook, '"asd"')

    def test_put_str(self, notebook):
        # returns as string
        assert "'whatever'" == self.put_to_SoS(notebook, 'whatever')

    def test_get_num_array(self, notebook):
        assert '1 2 3' == self.get_from_SoS(notebook, '["1", "2", "3"]')