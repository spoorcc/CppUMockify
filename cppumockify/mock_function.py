#!/usr/bin/env python3

# Copyright (c) 2015, Marco Molteni.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import os.path
import argparse
import logging

from .common import MockError

logger = logging.getLogger(__name__)

class MockFunction():

    VOID_MOCK = '''
{return_type} {function}({args}) {{
    mock().actualCall("{function}"){with_parameters};
}}'''.lstrip("\n")

    NON_VOID_MOCK = '''
{return_type} {function}({args}) {{
    mock().actualCall("{function}"){with_parameters};
    if mock().hasReturnValue() {{
        return mock().{return_value};
    }}
    return WRITEME;
}}'''.lstrip("\n")

    RETURN_VALUES = {
        # All the return values supported by CppUMock.
        'int':               'intReturnValue()',
        'unsigned int':      'unsignedIntReturnValue()',
        'long int':          'longIntReturnValue()',
        'unsigned long int': 'unsignedLongIntReturnValue()',
        'const char*':       'stringReturnValue()',
        'double':            'doubleReturnValue()',
        'void*':             'pointerReturnValue()',
        'const void*':       'constPointerReturnValue()',

        # Synthetic case
        'char*':             'pointerReturnValue()',
    }

    def __init__(self, func_to_mock):

        args, with_parameters = self._generate_args(func_to_mock.args)

        if func_to_mock.return_type == 'void':
            self.mock = self.VOID_MOCK.format(
                return_type=func_to_mock.return_type,
                function=func_to_mock.name,
                args=args,
                with_parameters=with_parameters)
        elif func_to_mock.return_type in self.RETURN_VALUES:
            self.mock = self.NON_VOID_MOCK.format(
                return_type=func_to_mock.return_type,
                function=func_to_mock.name,
                args=args,
                with_parameters=with_parameters,
                return_value=self.RETURN_VALUES[func_to_mock.return_type])
        else:
            raise MockError("Internal error, cannot handle: [{0}]".format(
                func_to_mock.return_type))

    def generate(self):
        return self.mock

    def _generate_args(self, param_list):
        ''' Generate the arguments '''
        if not param_list:
            return '', ''
        args = ''
        with_parameters = ''
        comma = ''
        for param_name, param_type in param_list:
            args += '{comma}{param_type} {param_name}'.format(
                comma=comma,
                param_type=param_type,
                param_name=param_name)
            with_parameters += \
                '\n        .withParameter("{0}", {0})'.format(param_name)
            comma = ', '

        return args, with_parameters


