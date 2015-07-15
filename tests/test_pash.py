#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pash
----------------------------------

Tests for `pash` module.
"""

import py.test
from pash import pash

proc = pash.ShellProc()
proc.run('ls')

def test_no_newline():
    assert proc.get_val('stdout')[-1] != '\n'
