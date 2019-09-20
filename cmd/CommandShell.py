# -*- coding: utf-8 -*-
"""Command Line Interface

Usage:
    run -h | --help
    run -v | -V | --version
    run start
    run stop

Commands:
    start
    stop

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


def colorize(s, color):
    color = eval(f'Fore.{color.upper()}')
    return f'{color}{s}{Style.RESET_ALL}'


class QuitException(Exception):
    pass


class ArgsException(Exception):
    pass


class CommandShell(cmd.Cmd):
    """Common command shell interface."""
    clear = lambda: os.system("cls" if platform.system().lower() == "windows" else "clear")

    def __init__(self, name):
        """
        Create common shell class
        """
        cmd.Cmd.__init__(self)
        self.intro = """============================================================================
        [L] Process List.
        [S] Process Status.
        [A] Admin Console access."""
        self.help_text = "press <Tab> to expand command or type ? to get any helps."
        self.prompt = f'{colorize(name, "lightgreen_ex")} > '

    def emptyline(self):
        """빈 입력값인 경우 마지막 명령어를 실행하는게 기본이나 마지막 명령어 반복을 막기 위해 해당 메서드 재정의"""
        pass

    def default(self, line):
        """입력값의 맞는 실행 함수가 없는 경우 실행"""
        self.clear()
        print(self.help_text)
        pass

#    def preloop(self):
#        print(f'{__name__}')
#
#    def precmd(self, line):
#        clear()
#        print(f'{__name__}')

    def do_execute(self, line):
        """Just echo"""
        print(f"{__name__} : {line}")

    def _quit(self):
        raise QuitException("quit")

    def do_exit(self, line):
        return self._quit()

    def do_quit(self, line):
        return self._quit()

    def do_EOF(self, line):
        return self._quit()

    def cmdloop(self, intro=None):
        while True:
            try:
                self.clear()
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

