#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import tempfile
from sos_notebook.test_utils import NotebookTest


class TestInterface(NotebookTest):

    def test_prompt_color(self, notebook):
        '''test color of input and output prompt'''
        idx = notebook.call(
            '''\
            echo this is bash
            ''', kernel="Bash")
        assert [230, 238, 255] == notebook.get_input_backgroundColor(idx)
        assert [230, 238, 255] == notebook.get_output_backgroundColor(idx)

    def test_cd(self, notebook):
        '''Support for change of directory with magic %cd'''
        output1 = notebook.check_output('pwd', kernel="Bash")
        notebook.call('%cd ..', kernel="SoS")
        output2 = notebook.check_output('pwd', kernel="Bash")
        assert len(output1) > len(output2)
        assert output1.startswith(output2)
        #
        # cd to a specific directory
        tmpdir = os.path.join(tempfile.gettempdir(), 'somedir')
        os.makedirs(tmpdir, exist_ok=True)
        notebook.call(f'%cd {tmpdir}', kernel="SoS")
        output = notebook.check_output('pwd', kernel="Bash")
        assert os.path.realpath(tmpdir) == os.path.realpath(output)
