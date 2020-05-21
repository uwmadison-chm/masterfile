#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

"""
Main script for masterfile operations.

Uses argparse and subcommands, controls like git.
"""

from __future__ import absolute_import, unicode_literals

import argparse


def make_parser():
    parser = argparse.ArgumentParser(prog='masterfile')
    parser.add_argument(
        '-v',
        '--verbose',
        help='Display debugging output',
        action="store_true")
    subparsers = parser.add_subparsers(dest="subcommand")

    create = subparsers.add_parser('create', help='Create blank dictionary')
    create.add_argument(
        'masterfile_path', help="Path to the masterfile to use")
    create.add_argument(
        'out_file', help="Path to the output file or - for STDOUT")

    pretty = subparsers.add_parser(
        'pretty', help='Create pretty dictionary, reformatting to contain every masterfile column. This is useful for feeding into Excel and browsing or searching around.')  # noqa
    pretty.add_argument(
        'masterfile_path', help="Path to the masterfile to use")
    pretty.add_argument(
        'out_file', help="Path to the output file or - for STDOUT")

    join = subparsers.add_parser('join', help='Make joined data')
    join.add_argument(
        'masterfile_path', help="Path to the masterfile to use")
    join.add_argument(
        'out_file', help="Path to the output file or - for STDOUT")

    extract = subparsers.add_parser('extract', help='Extract masterfile data')
    extract.add_argument(
        '-s', '--skip',
        metavar='ROWS',
        type=int,
        default=0,
        help="Skip <ROWS> data columns")
    extract.add_argument(
        '--index_column',
        metavar='COL',
        help="Use <COL> as the input's index column")
    extract.add_argument(
        'masterfile_path', help="Path to the masterfile to use")
    extract.add_argument(
        'csv_file', help="Path to the CSV input")
    extract.add_argument(
        'out_file', help="Path to the output file or - for STDOUT")

    validate = subparsers.add_parser('validate', help='Validate masterfile')
    validate.add_argument(
        'masterfile_path', help="Path to the masterfile to use")
    validate.add_argument(
        'file', nargs="*", help="Any additional files you wish to check")

    subparsers.add_parser(
        'dos',
        help=r'Text-to-DOS conversion, using stdin and stdout. ' +
        r'Changes line endings (\r, \n, \r\n) to DOS-style (\r\n). ' +
        r'Note: Also strips the UTF-8 signature (\xEF\xBB\xBF) from the start of files.') # noqa

    return parser


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "extract":
        from masterfile.scripts import extract
        return extract.main(args)
    elif args.subcommand == "create":
        from masterfile.scripts import create
        return create.main(args)
    elif args.subcommand == "pretty":
        from masterfile.scripts import pretty
        return pretty.main(args)
    elif args.subcommand == "join":
        from masterfile.scripts import join
        return join.main(args)
    elif args.subcommand == "validate":
        from masterfile.scripts import validate
        return validate.main(args)
    elif args.subcommand == "dos":
        from masterfile.scripts import text_to_dos
        return text_to_dos.main()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
