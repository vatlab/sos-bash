#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

#
# NOTE: for some namespace reason, this test can only be tested using
# nose.
#
# % nosetests test_kernel.py
#
#
import os
import unittest
from ipykernel.tests.utils import execute, wait_for_idle
from sos_notebook.test_utils import sos_kernel, get_result

class TestBashKernel(unittest.TestCase):
    #
    # Beacuse these tests would be called from sos/test, we
    # should switch to this directory so that some location
    # dependent tests could run successfully
    #
    def setUp(self):
        self.olddir = os.getcwd()
        if os.path.dirname(__file__):
            os.chdir(os.path.dirname(__file__))

    def tearDown(self):
        os.chdir(self.olddir)

    def testGetDataFromBash(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            execute(kc=kc, code='''
null_var = None
num_var = 123
logic_var = True
char_var = '123'
char_arr_var = ['1', '2', '3']
list_var = [1, 2, '3']
dict_var = dict(a=1, b=2, c='3')
set_var = {1, 2, '3'}
''')
            wait_for_idle(kc)
            execute(kc=kc, code='''
%use Bash
%get null_var num_var logic_var char_var char_arr_var list_var dict_var set_var
%dict -r
%put null_var num_var logic_var char_var char_arr_var list_var dict_var set_var
%use sos
%dict null_var num_var logic_var char_var char_arr_var list_var dict_var set_var
''')
            res = get_result(iopub)
            self.assertEqual(res['null_var'], '')
            self.assertEqual(res['num_var'], '123')
            self.assertEqual(res['logic_var'], 'TRUE')
            self.assertEqual(res['char_var'], '123')
            self.assertEqual(res['char_arr_var'], '1 2 3')
            self.assertEqual(res['list_var'], '1 2 3')
            self.assertEqual(sorted(res['dict_var']), [' ', ' ', 'a', 'b', 'c'])
            self.assertEqual(sorted(res['set_var']), [' ', ' ', '1', '2', '3'])

    def testPutBashDataToPython(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='%use Bash')
            wait_for_idle(kc)
            execute(kc=kc, code="export null_var=")
            wait_for_idle(kc)
            execute(kc=kc, code="vvv=12345")
            wait_for_idle(kc)
            execute(kc=kc, code="export num_var=123")
            wait_for_idle(kc)
            execute(kc=kc, code="%put null_var num_va vvv")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict null_var num_var vvv")
            res = get_result(iopub)
            self.assertEqual(res['null_var'], '')
            self.assertEqual(res['num_var'], '123')
            self.assertEqual(res['vvv'], '12345')
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)


if __name__ == '__main__':
    unittest.main()
