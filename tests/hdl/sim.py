#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Wrapper for HDl simulators.

All simulator executables must be visible in PATH.
"""

import os
import shutil
import glob
import subprocess
import argparse
from pathlib import Path


class Simulator:
    """Simulator wrapper"""
    def __init__(self, tool='icarus'):
        if tool not in ['icarus', 'modelsim']:
            raise ValueError("Unknown simulator tool '%s'" % tool)
        self._tool = tool
        self._cwd = os.path.dirname(os.path.realpath(__file__))

        self.worklib = 'worklib'
        self.top = 'top'
        self.sources = []
        self.defines = []
        self.incdirs = []

    def run(self, gui=True):
        """Run simulation"""
        # remove previous simulation artifacts
        self.clean()
        # add behavioral modules
        self.sources += [
            str(Path(self._cwd) / 'beh' / 'apb.sv')
        ]
        self.defines += [
            'TOP_NAME=' + self.top
        ]
        self.incdirs += [
            str(Path(self._cwd) / 'beh')
        ]
        # run selected simulator
        if self._tool == 'icarus':
            return self._run_icarus(gui)
        elif self._tool == 'modelsim':
            return self._run_modelsim(gui)

    def clean(self):
        """Remove all build artifacts"""
        workdir = Path(self._cwd)
        # remove files
        rm_files = []
        rm_files += glob.glob(str(workdir / '*.vvp'))
        rm_files += glob.glob(str(workdir / '*.vcd'))
        rm_files += glob.glob(str(workdir / '*.tcl'))
        rm_files += glob.glob(str(workdir / '*.ini'))
        rm_files += glob.glob(str(workdir / '*.wlf'))
        rm_files += glob.glob(str(workdir / '*.do'))
        rm_files += glob.glob(str(workdir / '*.vstf'))
        rm_files += glob.glob(str(workdir / 'transcript'))
        for f in rm_files:
            os.remove(f)
        # remove directories
        rm_dirs = []
        rm_dirs += [workdir / 'worklib']
        for d in rm_dirs:
            if d.exists() and d.is_dir():
                shutil.rmtree(d)

    def _get_file_ext(self, path):
        _, ext = os.path.splitext(path)
        return ext.lower()

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
        # prepare compile script
        defines = ' '.join(['+define+' + define for define in self.defines])
        incdirs = ' '.join(['+incdir+' + incdir for incdir in self.incdirs])
        sources = ''
        for src in self.sources:
            ext = self._get_file_ext(src)
            if ext in ['.v', '.sv']:
                sources += 'vlog %s %s -sv -timescale \"1 ns / 1 ps\" %s\n' % (defines, incdirs, src)
            elif ext == 'vhd':
                sources += 'vcom -93 %s\n' % src
        if not gui:
            run = 'run -all'
        else:
            run = ''
        compile_tcl = """
proc rr  {{}} {{
  write format wave -window .main_pane.wave.interior.cs.body.pw.wf wave.do
  uplevel #0 source compile.tcl
}}
proc q  {{}} {{quit -force                  }}
vlib {worklib}
vmap work {worklib}
{sources}
eval vsim {worklib}.{top}
if [file exist wave.do] {{
  source wave.do
}}
{run}
"""
        with open(Path(self._cwd) / 'compile.tcl', 'w') as f:
            f.writelines(compile_tcl.format(worklib=self.worklib,
                                            top=self.top,
                                            incdirs=incdirs,
                                            sources=sources,
                                            defines=defines,
                                            run=run))
        vsim_args = '-do compile.tcl'
        if not gui:
            vsim_args += ' -c'
            vsim_args += ' -onfinish exit'
        else:
            vsim_args += ' -onfinish stop'
        self._exec('vsim', vsim_args)


class Simulation:
    """Run simulation with command line parameters."""
    def __init__(self, default_tb='tb_default', default_tool='icarus', default_gui=True, tb_dict={}):
        self.tb_dict = tb_dict

        self.args_parser = argparse.ArgumentParser()
        self.args_parser.add_argument('-t',
                                      default=default_tb,
                                      metavar='<name>',
                                      dest='tb',
                                      help="testbench <name>; default is '%s'" % default_tb)
        self.args_parser.add_argument('-s',
                                      default=default_tool,
                                      metavar='<name>',
                                      dest='tool',
                                      help="simulation tool <name>; default is '%s'" % default_tool)
        self.args_parser.add_argument('-b',
                                      default=default_gui,
                                      dest='gui',
                                      action='store_false',
                                      help='enable batch mode (no GUI)')

    def run(self):
        args = self.args_parser.parse_args()
        try:
            print("Start simulation for testbench '%s'" % args.tb)
            self.tb_dict[args.tb](tool=args.tool, gui=args.gui)
        except KeyError:
            raise ValueError("Unknown testbench name '%s'" % args.tb)


if __name__ == '__main__':
    sim = Simulator()
    sim.clean()
