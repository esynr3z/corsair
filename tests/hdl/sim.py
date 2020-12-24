#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Wrapper for HDl simulators.

All simulator executables must be visible in PATH.
"""

import os
import glob
import subprocess
from pathlib import Path


class Simulator:
    """Simulator wrapper"""
    def __init__(self, tool='icarus'):
        if tool not in ['icarus', 'modelsim']:
            raise ValueError("Unknown simulator tool '%s'" % tool)
        self._tool = tool
        self._cwd = os.path.dirname(os.path.realpath(__file__))

        self.sources = []
        self.defines = []
        self.incdirs = []
        self.worklib = 'worklib'
        self.top = 'top'

    def run(self, gui=True):
        """Run simulation"""
        self.clean()
        if self._tool == 'icarus':
            return self._run_icarus(gui)
        elif self._tool == 'modelsim':
            return self._run_modelsim(gui)

    def clean(self):
        """Remove all build artifacts"""
        workdir = Path(self._cwd)
        rm_list = []
        rm_list += glob.glob(str(workdir / '*.vvp'))
        rm_list += glob.glob(str(workdir / '*.vcd'))
        for path in rm_list:
            os.remove(path)

    def _exec(self, prog, args):
        """Execute external program.

        Args:
            prog : string with program name
            args : string with program arguments
        """
        exec_str = prog + " " + args
        print(exec_str)
        child = subprocess.Popen(exec_str.split(), cwd=self._cwd, stdout=subprocess.PIPE)
        self.stdout = child.communicate()[0].decode("utf-8")
        print(self.stdout)
        self.retcode = child.returncode
        if self.retcode:
            raise RuntimeError("Simulation failed at '%s' with return code %d!" % (exec_str, self.retcode))

    def _run_icarus(self, gui=True):
        """Run Icarus + GTKWave"""
        print('Run Icarus')
        # elaborate
        elab_args = ''
        elab_args += ' '.join(['-I ' + incdir for incdir in self.incdirs]) + ' '
        elab_args += ' '.join(['-D ' + define for define in self.defines]) + ' '
        elab_args += '-g2005-sv -s %s -o %s.vvp' % (self.top, self.worklib) + ' '
        elab_args += ' '.join(self.sources)
        self._exec('iverilog', elab_args)
        # simulate
        self._exec('vvp', '%s.vvp -lxt2' % self.worklib)
        # show waveforms
        if gui:
            self._exec('gtkwave', 'dump.vcd')

    def _run_modelsim(self, gui=True):
        """Run Modelsim"""
        print('Run Modelsim')


if __name__ == '__main__':
    sim = Simulator()
    sim.clean()
