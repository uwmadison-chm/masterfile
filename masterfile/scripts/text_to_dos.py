#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Changes line endings (\r, \n, \r\n) to DOS-style (\r\n). Writes to stdout.

Note: Also strips the UTF-8 signature (\xEF\xBB\xBF) from the start of files.
"""

import sys
import re


def main():
    PY3K = sys.version_info >= (3, 0)

    if PY3K:
        stdin = sys.stdin.buffer
        stdout = sys.stdout.buffer
    else:
        stdin = sys.stdin
        stdout = sys.stdout
        # Python 2 on Windows opens sys.stdin in text mode, and
        # binary data that read from it becomes corrupted on \r\n
        if sys.platform == 'win32':
            # set sys.stdin to binary mode
            import os, msvcrt # NOQA
            msvcrt.setmode(stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(stdout.fileno(), os.O_BINARY)

    utf8_bom = b'\xEF\xBB\xBF'
    line_ending_re = re.compile(b'\r\n|\r|\n')

    input_data = stdin.read()
    no_bom = input_data
    if input_data.startswith(utf8_bom):
        no_bom = input_data.replace(utf8_bom, b'', 1)

    stdout.write(line_ending_re.sub(b'\r\n', no_bom))
    if not no_bom.endswith(b'\r\n'):
        stdout.write(b'\r\n')


if __name__ == '__main__':
    main()
