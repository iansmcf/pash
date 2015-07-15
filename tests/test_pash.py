#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pash
----------------------------------

Tests for `pash` module.
"""

import py.test
import pash

proc = pash.ShellProc()
proc.run('ls ~')

""" Test that stdout and stderr do not have terminal endlines.
    stderr has no value, it will be None instead. """
def test_no_newline():
    try:
        assert proc.get_val('stdout')[-1] != '\n'
    except TypeError:
        assert proc.get_val('stdout') == None
    try:
        assert proc.get_val('stderr')[-1] != '\n'
    except TypeError:
        assert proc.get_val('stderr') == None

""" Test that running a command returns a value """
def returns_stdout():
    returned = proc.run('ls ~')
    assert returned != False








 
