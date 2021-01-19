#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""HDL simulation utilities.

All simulator executables must be visible in PATH.
"""

import subprocess
import argparse
from pathlib import Path


def file_ext(filepath):
    """Get file extension from filepath"""
    return Path(filepath).suffix


def parent_dir(filepath):
    """Get parent directory path from filepath"""
    return Path(filepath).resolve().parent


def make_dir(name):
    """Make directory with specified name"""
    return Path(name).mkdir()


def path_join(*other):
    """Add each of other argumetns to path in turn"""
    return Path().joinpath(*other)


def remove_tree(dirpath):
    """Remove an entire directory tree if it exists"""
    p = Path(dirpath)
    if p.exists() and p.is_dir():
        for child in p.glob('*'):
            if child.is_file():
                child.unlink()
            else:
                remove_tree(child)
        p.rmdir()


def get_define(name, defines):
    """Return define value from defines list"""
    try:
        return next(d for d in defines if name in d).split('=')[-1]
    except StopIteration:
        return None


def write_memfile(path, data):
    """Write data to memory file (can be loaded with $readmemh)"""
    with Path(path).open(mode='w', encoding="utf-8") as memfile:
        memfile.writelines(['%x\n' % d for d in data])


class Simulator:
    """Simulator wrapper"""
    def __init__(self, name='icarus', gui=True, cwd='work', passed_marker='!@# TEST PASSED #@!'):
        self.gui = gui
        self.passed_marker = passed_marker

        self.cwd = Path(cwd).resolve()
        if parent_dir(__file__) == self.cwd:
            raise ValueError("Wrong working directory '%s'" % self.cwd)

        self.name = name
        self._runners = {'modelsim': self._run_modelsim,
                         'vivado': self._run_vivado}
        if self.name not in self._runners.keys():
            raise ValueError("Unknown simulator tool '%s'" % self.name)

        self.worklib = 'worklib'
        self.top = 'top'
        self.sources = []
        self.defines = []
        self.incdirs = []

        self.stdout = ''
        self.retcode = 0

    def setup(self):
        """Prepare working directory"""
        remove_tree(self.cwd)
        make_dir(self.cwd)

    def run(self):
        """Run selected simulator"""
        # some preprocessing
        self.sources = [str(Path(filepath).resolve()) for filepath in self.sources]
        self.incdirs = [str(Path(dirpath).resolve()) for dirpath in self.incdirs]
        self.defines += ['TOP_NAME=%s' % self.top, 'SIM']
        # run simulation
        self._runners[self.name]()

    def get_define(self, name):
        """Return define value from defines list"""
        return get_define(name, self.defines)

    @property
    def is_passed(self):
        return self.passed_marker in self.stdout

    def _exec(self, prog, args):
        """Execute external program.

        Args:
            prog : string with program name
            args : string with program arguments
        """
        exec_str = prog + " " + args
        print(exec_str)
        child = subprocess.Popen(exec_str.split(), cwd=self.cwd, stdout=subprocess.PIPE)
        self.stdout = child.communicate()[0].decode("utf-8")
        print(self.stdout)
        self.retcode = child.returncode
        if self.retcode:
            raise RuntimeError("Execution failed at '%s' with return code %d!" % (exec_str, self.retcode))

    def _run_modelsim(self):
        """Run Modelsim"""
        print('Run Modelsim (cwd=%s)' % self.cwd)
        print(' '.join([d for d in self.defines]))
        # compile sources
        defines = ' '.join(['+define+' + define for define in self.defines])
        incdirs = ' '.join(['+incdir+' + incdir for incdir in self.incdirs])
        scr_compile = []
        for src in self.sources:
            ext = file_ext(src)
            if ext in ['.v', '.sv']:
                scr_compile += [{
                    'tool': 'vlog',
                    'args': '-suppress 2902 %s %s -sv -timescale 1ns/1ps %s' % (defines, incdirs, src)
                }]
            elif ext == 'vhd':
                scr_compile += [{
                    'tool': 'vcom',
                    'args': '-93 %s\n' % src
                }]
        self._exec('vlib', self.worklib)
        self._exec('vmap', 'work %s' % self.worklib)
        for src in scr_compile:
            self._exec(src['tool'], src['args'])
        # prepare simulation
        if not self.gui:
            run = 'run -all'
        else:
            run = ''
        sumulate_tcl = """
proc rr  {{}} {{
  write format wave -window .main_pane.wave.interior.cs.body.pw.wf wave.do
{sources}
  uplevel #0 source simulate.tcl
}}
proc q  {{}} {{quit -force}}
eval vsim {worklib}.{top}
if [file exist wave.do] {{
  source wave.do
}}
{run}
"""
        sources = ''
        for src in scr_compile:
            ''.join(["  %s %s\n" % (src['tool'], src['args']) for src in scr_compile])
        with path_join(self.cwd, 'simulate.tcl').open(mode='w', encoding="utf-8") as f:
            f.write(sumulate_tcl.format(
                worklib=self.worklib,
                top=self.top,
                incdirs=incdirs,
                sources=''.join(["  %s %s\n" % (src['tool'], src['args']) for src in scr_compile]),
                defines=defines,
                run=run
            ))
        vsim_args = '-do simulate.tcl'
        if not self.gui:
            vsim_args += ' -c'
            vsim_args += ' -onfinish exit'
        else:
            vsim_args += ' -onfinish stop'
        self._exec('vsim', vsim_args)

    def _run_vivado(self):
        """Run Vivado simulator"""
        print('Run Vivado (cwd=%s)' % self.cwd)
        print(' '.join([d for d in self.defines]))
        # prepare and run elaboration
        elab_args = "--debug all --incr --prj files.prj %s.%s " % (self.worklib, self.top)
        elab_args += ' '.join(['-d ' + define for define in self.defines]) + ' '
        elab_args += ' '.join(['-i ' + incdir for incdir in self.incdirs])
        sources = ''
        for src in self.sources:
            ext = file_ext(src)
            if ext == '.sv':
                sources += 'sv %s %s\n' % (self.worklib, src)
            elif ext == '.v':
                sources += 'verilog %s %s\n' % (self.worklib, src)
            elif ext == 'vhd':
                sources += 'vhdl %s %s\n' % (self.worklib, src)
        with path_join(self.cwd, 'files.prj').open(mode='w', encoding="utf-8") as f:
            f.write(sources)
        self._exec('xelab', elab_args)
        # prepare and run simulation
        reinvoke_tcl = """
proc rr {{}} {{
    exec xelab {elab_args}
    save_wave_config work
    close_sim
    source xsim.dir/{worklib}.{top}/xsim_script.tcl
}}
"""
        with path_join(self.cwd, 'reinvoke.tcl').open(mode='w', encoding="utf-8") as f:
            f.write(reinvoke_tcl.format(elab_args=elab_args, worklib=self.worklib, top=self.top))
        work_wcfg = """<?xml version="1.0" encoding="UTF-8"?>
<wave_config>
   <wave_state>
   </wave_state>
</wave_config>
"""
        with path_join(self.cwd, 'work.wcfg').open(mode='w', encoding="utf-8") as f:
            f.write(work_wcfg)
        sim_args = "%s.%s" % (self.worklib, self.top)
        if not self.gui:
            sim_args += ' --R'
        else:
            sim_args += ' --gui --t reinvoke.tcl --view work.wcfg'
        self._exec('xsim', sim_args)


class CliArgs:
    """Parse command line parameters for simulation"""
    def __init__(self, default_test='test', default_simtool='modelsim', default_gui=True, default_defines=[]):
        self.args_parser = argparse.ArgumentParser()
        self.args_parser.add_argument('-t',
                                      default=default_test,
                                      metavar='<name>',
                                      dest='test',
                                      help="test <name>; default is '%s'" % default_test)
        self.args_parser.add_argument('-s',
                                      default=default_simtool,
                                      metavar='<name>',
                                      dest='simtool',
                                      help="simulation tool <name>; default is '%s'" % default_simtool)
        self.args_parser.add_argument('-b',
                                      default=default_gui,
                                      dest='gui',
                                      action='store_false',
                                      help='enable batch mode (no GUI)')
        self.args_parser.add_argument('-d',
                                      default=default_defines,
                                      metavar='<def>',
                                      dest='defines',
                                      nargs='+',
                                      help="define <name>; option can be used multiple times")

    def parse(self):
        return self.args_parser.parse_args()
