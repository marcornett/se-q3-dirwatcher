#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "marcornett"

import sys
import logging
import argparse


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return

# Do break up your code into small functions such as
# scan_single_file(), detect_added_files(),
# detect_removed_files(), and watch_directory().


def watch_directory(path, magic_string, extension, interval):
    # Your code here
    return


def create_parser():
    """Creates command line parser object to accept one argument."""
    parser = argparse.ArgumentParser()
    # todo if no directory log dirtory XXXX does not exist
    parser.add_argument('-dir', '--directory', help='Directory to watch.')
    parser.add_argument('-ext', '--extension',
                        help='Extension type to look for.')
    # todo polling interval default to 1.0 seconds
    parser.add_argument('-int', '--interval',
                        help='Polling interval. Default 1.0 seconds')
    parser.add_argument('magic', help='Magic text to search for')

    return parser


def signal_handler(sig_num, frame):
    # Your code here
    return


def main(args):
    """Main driver code for dirwatcher."""
    # logging.basicConfig(level=logging.INFO)
    # logging.info("args:", args)
    parser = create_parser()

    ns = parser.parse_args(args)

    if not ns:
        # TODO find out if sys.exit is allowed here
        parser.print_usage()
        sys.exit(1)

    directory = ns.directory
    extension = ns.extension
    interval = ns.interval
    magic_word = ns.magic

    # TODO call functions using args


if __name__ == '__main__':
    main(sys.argv[1:])
