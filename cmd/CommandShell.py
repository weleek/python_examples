# -*- coding: utf-8 -*-
"""Command Line Interface

Usage:
    run -h | --help
    run -i | --interactive
    run start [process name]
    run stop [process name]

Commands:
    start                       Program Start.
    stop                        Program Stop.

Options:
    -v -V --version             show version info.
    -i --interactive            use interactive console.
"""

import os
import sys
import platform
import cmd
from docopt import docopt
from colorama import Fore, Style


def parse_command(argv=None):
    return docopt(__doc__, argv, version='0.0.1')


def run_subcommand(args):
    for k, v in args.items():
        if k[:2] == '--':  # 옵션 건너뛰기
            continue
        if v:
            os.system(f'echo "call {k}"')


def colorize(s, color):
    color = eval(f'Fore.{color.upper()}')
    return f'{color}{s}{Style.RESET_ALL}'


class QuitException(Exception):
    pass


class ArgsException(Exception):
    pass


class CommandShell(cmd.Cmd):
    """Common command shell interface."""

    def _clear(self):
        os.system("cls" if platform.system().lower() == "windows" else "clear")

    def __init__(self, name):
        """
        Create common shell class
        """
        cmd.Cmd.__init__(self)
        self.intro = """================================ Test Cli Program ==============================================
[L] Process List.
[S] Process Status.
[Q] Quit."""
        self.help_text = "press <Tab> to expand command or type ? to get any helps."
        self.prompt = f'{colorize(name, "lightgreen_ex")} > '
        self.choice = False

    def emptyline(self):
        """빈 입력값인 경우 마지막 명령어를 실행하는게 기본이나 마지막 명령어 반복을 막기 위해 해당 메서드 재정의"""
        self._clear()
        print(self.intro)
        print("Please select a Menu")
        pass

    def default(self, line):
        """입력값의 맞는 실행 함수가 없는 경우 실행"""
        if not self.choice:
            self._clear()
            print(f"Please select a Menu.\nDoes not exists. [{line}]")
        pass

    """onecmd 함수를 재정의 하였기 때문에 아래 함수를 이용하여 기능을 이용하지 않으므로 주석 처리한다."""

    #    def preloop(self):
    #       """기본 loop가 돌기 이전 실행 되는 루프"""
    #        print(f'{__name__}')

    #    def precmd(self, line):
    #        """명령어 처리 이전에 제일 처음 실행 된다."""
    #        self._clear()
    #        switch = line.upper()
    #        if switch == 'S':
    #            self.choice = True
    #            print(f'choice menu : [{line}]')
    #        elif switch == 'L':
    #            self.choice = True
    #            print(f'choice menu : [{line}]')
    #        elif switch == 'Q':
    #            self.choice = True
    #            self.do_exit(line)
    #        return line

    def get_cmd(self, cmd):
        """기본 규칙인 함수 앞에 do_ 를 붙인 함수명을 반환하지 않도록 커스텀 하기 위한 함수."""
        func_list = self.get_names()
        cmd = f'cmd_{cmd}'
        for func_name in func_list:
            if func_name.startswith(cmd):
                cmd = func_name
                break
        return cmd

    def onecmd(self, line):
        """기본 명령 실행 함수."""
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, self.get_cmd(cmd))
            except AttributeError:
                return self.default(line)
            return func(arg)

    def cmd_list_of_process(self, arg):
        """[L] Show Process List."""
        self._clear()
        print(f'List')

    def cmd_status_of_process(self, arg):
        """[S] Show Process Status."""
        self._clear()
        print(f'Status')

    def cmd_quit(self, arg):
        return self._quit()

    def _quit(self):
        raise QuitException("quit")

    def cmdloop(self, intro=None):
        while True:
            try:
                self._clear()
                cmd.Cmd.cmdloop(self, intro)
            except QuitException as qe:
                print(f'{qe}')
                break
            except KeyboardInterrupt:
                print('Program Exit...')
                break
            except ArgsException as e:
                print(f"Error parsing arguments!\n {e}")
                continue
            except Exception as e:
                print(f'Unknown Exception : {e}')
                break
