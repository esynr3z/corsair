#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test of examples.
"""

import os
import subprocess
import pytest
from pathlib import Path


def test_examples(tmpdir):
    # prepare examples
    res = subprocess.run(["cp", "-R", "examples", str(tmpdir)])
    assert res.returncode == 0

    # prepare environment - to make sure Makefile will find corsair repo
    my_env = os.environ.copy()
    if 'PYTHONPATH' not in my_env.keys():
        my_env['PYTHONPATH'] = ""
    my_env['PYTHONPATH'] = "%s:%s" % (str(Path(os.getcwd()).absolute()), my_env['PYTHONPATH'])
    examples_path = str(tmpdir.join('examples'))

    # clean examples
    res = subprocess.run(["make", "-C", examples_path, "clean"], env=my_env)
    assert res.returncode == 0

    # build examples
    res = subprocess.run(["make", "-C", examples_path], env=my_env)
    assert res.returncode == 0
