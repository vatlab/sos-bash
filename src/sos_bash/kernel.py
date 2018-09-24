#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

from collections.abc import Sequence
from sos.utils import short_repr, env

#
#  support for %get
#
#  Converting a Python object to a R expression that will be executed
#  by the R kernel.
#
#
def _Bash_repr(obj):
    if isinstance(obj, bool):
        return 'TRUE' if obj else 'FALSE'
    elif isinstance(obj, (int, float)):
        return repr(obj)
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, Sequence):
        if len(obj) == 0:
            return ''
        return ' '.join(_Bash_repr(x) for x in obj)
    elif obj is None:
        return ''
    elif isinstance(obj, dict):
        return ' '.join(_Bash_repr(x) for x in obj.keys())
    elif isinstance(obj, set):
        return ' '.join(_Bash_repr(x) for x in obj)
    else:
        return repr('Unsupported datatype {}'.format(short_repr(obj)))

class sos_Bash:
    supported_kernels = {'Bash': ['bash']}
    background_color = '#E6EEFF'
    options = {}
    cd_command = 'cd {dir}'

    def __init__(self, sos_kernel, kernel_name='bash'):
        self.sos_kernel = sos_kernel
        self.kernel_name = kernel_name
        self.init_statements = ''

    def get_vars(self, names):
        for name in names:
            stmt = 'export {}={!r}'.format(name, _Bash_repr(env.sos_dict[name]))
            self.sos_kernel.run_cell(stmt, True, False, on_error='Failed to get variable {}'.format(name))

    def put_vars(self, items, to_kernel=None):
        # first let us get all variables with names starting with sos
        response = self.sos_kernel.get_response('set', ('stream'))
        response = [x[1]['text'].split('=', 1) for x in response if '=' in x[1]['text']]
        all_vars = {x:y.strip() for x,y in response if x.startswith('sos') or x in items}
        all_vars = {x:y.strip("'") if y.startswith("'") and y.endswith("'") else y for x,y in all_vars.items()}

        for item in items:
            if item not in all_vars:
                self.sos_kernel.warn('Variable not exist: {}'.format(item))

        return all_vars



