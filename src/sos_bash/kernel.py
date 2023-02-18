#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

from collections.abc import Sequence

from sos.utils import env, short_repr


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
        return repr(f'Unsupported datatype {short_repr(obj)}')


class sos_Bash:
    supported_kernels = {'Bash': ['bash', 'calysto_bash'], 'Zsh': ['zsh']}
    background_color = {'Bash': '#E6EEFF', 'Zsh': '#E6EEFA'}
    options = {}
    cd_command = 'cd {dir}'

    def __init__(self, sos_kernel, kernel_name='bash'):
        self.sos_kernel = sos_kernel
        self.kernel_name = kernel_name
        self.init_statements = ''

    async def get_vars(self, names, as_var=None):
        for name in names:
            stmt = f'export {as_var if as_var else name}={_Bash_repr(env.sos_dict[name])!r}'
            env.log_to_file('KERNEL', f'Execute "{stmt}"')
            await self.sos_kernel.run_cell(stmt, True, False, on_error=f'Failed to get variable {name}')

    def put_vars(self, items, to_kernel=None, as_var=None):
        if not items:
            return {}
        # zsh does not handle set command well https://github.com/danylo-dubinin/zsh-jupyter-kernel/issues/12
        #
        if self.kernel_name == 'zsh':
            all_vars = {}
            for item in items:
                response = self.sos_kernel.get_response(f'[[ -v {item} ]] && echo {as_var if as_var else item}=${item}',
                                                        ('stream'))
                if not response:
                    self.sos_kernel.warn(f'Variable not exist: {item}')
                else:
                    text = response[0][1]['text']
                    if not text.startswith(f'{item}='):
                        self.sos_kernel.warn(f'Failed to get value of {item}: {text} returned')
                    text = text[len(item) + 1:].rstrip()
                    if text.startswith("'") and text.endswith("'"):
                        all_vars[item] = text.strip("'")
                    else:
                        all_vars[item] = text
        else:
            # first let us get all variables
            response = self.sos_kernel.get_response('set', ('stream'))
            # the output from bash is separated into multiple responses
            # while output from calyatal bash is a single one
            stdout = [x[1]['text'] for x in response if '=' in x[1]['text']]
            #
            # list of variables
            all_vars = []
            for text in stdout:
                all_vars.extend([x.split('=', 1) for x in text.splitlines() if '=' in x])

            all_vars = {
                as_var if as_var else x: y.strip("'") if y.startswith("'") and y.endswith("'") else y
                for x, y in all_vars
                if x in items
            }

            for item in items:
                if item not in all_vars:
                    self.sos_kernel.warn(f'Variable not exist: {item}')

        return all_vars
