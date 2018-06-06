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

"""
Simple script to generate a skeleton mock file and function for CppUMock.
It expects to be run in the directory containing the mocks.
"""

import logging

from pycparser import c_parser, c_ast

from .common import MockError

logger = logging.getLogger(__name__)

class Prototype():

    def __init__(self, prototype):
        ''' Prototype class takes a string prototype and makes function args, name and return type accessible '''

        self._parse_function_from_prototype(prototype)
        self._parse_return_type(self._func_decl)
        self._parse_all_parameters(self._func_decl.args.params)

    def _parse_function_from_prototype(self, prototype):
        ''' Parse the function from the prototype '''
        # Thanks to cdecl.py from pycparser
        parser = c_parser.CParser()
        try:
            ast = parser.parse(prototype)
        except c_parser.ParseError as exc:
            raise MockError("Parse error: '{0}' with input: '{1}'".format(
                str(exc), prototype))
        decl = ast.ext[-1]
        if not isinstance(decl, c_ast.Decl):
            raise MockError("Not a valid declaration: " + prototype)
        # decl.show(); print("")

        if not isinstance(decl.type, c_ast.FuncDecl):
            raise MockError("Not a function declaration: " + prototype)

        # storage is, for example, "static" in "static void f();"
        if decl.storage:
            storage = ' '.join(decl.storage)
            raise MockError("Cannot mock a function with storage: " + storage)

        self._func_decl = decl.type
        self.name = decl.name

    def _parse_return_type(self, func_decl):
        ''' Parses the type name from the function declaration '''

        pointer = False
        if isinstance(func_decl.type, c_ast.PtrDecl):
            # void* f(); =>
            # Decl: f, [], [], []
            #   FuncDecl:
            #     PtrDecl: []                   <== here
            #       TypeDecl: f, []
            #         IdentifierType: ['void']
            type_decl = func_decl.type.type
            pointer = True
        elif isinstance(func_decl.type, c_ast.TypeDecl):
            # void f(); =>
            # Decl: f, [], [], []
            #   FuncDecl:
            #     TypeDecl: f, []               <== here
            #       IdentifierType: ['void']
            type_decl = func_decl.type
        else:
            raise MockError("Internal error parsing: " + func_decl.name)

        identifier_type = type_decl.type

        # e.g.: "int" in "int f()"
        self.return_type = ' '.join(identifier_type.names)
        if pointer:
            self.return_type += '*'
        # e.g.: "const" in "const char* f()"
        try:
            self.return_type = type_decl.quals[0] + " " + self.return_type
        except IndexError:
            pass

    def _parse_all_parameters(self, params):
        self.args = []
        for decl in params:
            param_name, param_type = self._parse_single_param(decl)

            if param_name:
                self.args += [[param_name, param_type]]
            else:
                break # Void - stop parsing args

    def _parse_single_param(self, decl):
        
        # Decl: k, [], [], []
        #     TypeDecl: k, []
        #         IdentifierType: ['int']
        # Decl: i, [], [], []
        #     PtrDecl: []
        #         TypeDecl: i, []
        #             IdentifierType: ['char']
        # decl.show()
        param_name = decl.name
        if isinstance(decl.type, c_ast.TypeDecl):
            type_decl = decl.type
            identifier_type = type_decl.type
            param_type = identifier_type.names[0]
        elif isinstance(decl.type, c_ast.PtrDecl):
            type_decl = decl.type.type
            identifier_type = type_decl.type
            param_type = identifier_type.names[0] + '*'
        else:
            raise MockError("Internal error parsing arguments")

        if not param_name:
            # Unnamed void argument: "f(void);" ?
            if param_type == 'void':
                # FIXME Not 100% robust if other arguments are present
                return '', ''
            else:
                raise MockError("Cannot mock unnamed arguments. "
                                "Please rewrite the prototype")
        try:
            param_type = type_decl.quals[0] + " " + param_type
        except IndexError:
            pass

        return (param_name, param_type)

