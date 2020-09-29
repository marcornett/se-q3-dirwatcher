#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "marcornett"

import sys
import logging
import argparse
import signal
import time
import os


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

def create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return

# Do break up your code into small functions such as
# scan_single_file(), detect_added_files(),
# detect_removed_files(), and watch_directory().


def watch_directory(path, magic_string, extension, interval):
    print('calling watch_directory')
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
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # All log messages should contain timestamps.

    # exceptions, magic text found events,
    # files added or removed from watched dir,
    # and OS signal events.
    logger = create_logger()
    logger.warning('Received ' + signal.Signals(sig_num).name)
    # TODO log shutdown banner
    sys.exit(1)


def main(args):
    """Main driver code for dirwatcher."""

    # Register signals to catch
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Collect command line arguments
    parser = create_parser()
    ns = parser.parse_args(args)
    if not ns:
        # TODO find out if sys.exit is allowed here
        parser.print_usage()
        sys.exit(1)
    directory = ns.directory
    print(directory)
    # print(os.path.abspath(directory))
    extension = ns.extension
    magic_word = ns.magic
    interval = ns.interval

    # TODO log startup banner

    while True:
        try:
            print('working')
            watch_directory()
        except Exception:
            # This is an UNHANDLED exception
            # TODO Log an ERROR level message here
            pass
        else:
            pass
        finally:
            # Checks for provided interval
            if not interval:
                time.sleep(1)
            else:
                time.sleep(int(interval))


if __name__ == '__main__':
    main(sys.argv[1:])
