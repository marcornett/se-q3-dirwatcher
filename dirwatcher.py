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
import datetime
import os

file_dict = {}
exit_flag = False


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s \n%(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger.addHandler(handler)


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return


def scan_single_file(single_file, path):
    with open(os.path.join(path, single_file)) as f:
        file_content = f.readlines()
        print(file_content)

    # with open(f'{path}/{filename}', 'r') as f:
    #     file_contents = f.read()
    #     print(file_contents)
    #     f.seek()
    # TODO return seek location


def detect_added_files(path, new_read, file_dict):
    for f in new_read:
        if f not in file_dict:
            print(f'Added {f}')
            file_dict.update({f: 0})


def detect_removed_files(path, new_read, file_dict):
    for f in file_dict:
        if f not in new_read:
            print(f'Removed {f}')
            file_dict = new_read
            break


def watch_directory(path, magic_string, extension, interval):
    """Monitors given directory and reports back changes"""
    global file_dict
    new_read = {f: 0 for f in os.listdir(path)}
    detect_added_files(path, new_read, file_dict)
    detect_removed_files(path, new_read, file_dict)

    for f in file_dict:
        scan_single_file(f, path)

    # TODO Once you have synchronized your dictionary,
    # TODO it is time to iterate through all of its files and
    # TODO look for magic text, starting from the line number
    # TODO where you left off last time.
    # TODO The keys will be filenames
    # TODO and the values will be the last line number that was read during
    # TODO the previous polling iteration. Keep track of the last line read.
    # TODO report new files added to dictionary
    # TODO When opening and reading the file, skip over all the lines that
    # TODO you have previously examined.


def create_parser():
    """Creates command line parser object to accept one argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', '--directory', help='Directory to watch.')
    # TODO set default
    parser.add_argument('-ext', '--extension',
                        help='Extension type to look for.')
    parser.add_argument('-int', '--interval',
                        help='Polling interval. Default 1.0 seconds')
    parser.add_argument('magic', help='Magic text to search for')
    return parser


def signal_handler(sig_num, frame):
    """Handler for SIGTERM and SIGINT."""
    # uptime = datetime.datetime.now() - start_time
    global exit_flag
    logger.warning('Received ' + signal.Signals(sig_num).name)
    exit_flag = True


def main(args):
    """Main driver code for dirwatcher."""
    global exit_flag
    # Register signals to catch
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Collect command line arguments
    parser = create_parser()
    ns = parser.parse_args(args)
    if not ns:
        parser.print_usage()
        sys.exit(1)
    path = ns.directory
    extension = ns.extension
    magic_word = ns.magic

    if ns.interval:
        interval = int(ns.interval)
    else:
        interval = 1

    logger.info(f"""
-------------------------------------------------------------------
    Start {__file__}
-------------------------------------------------------------------
    """)
    global file_dict
    file_dict = {f: 0 for f in os.listdir(path)}
    while not exit_flag:
        time.sleep(interval)
        try:
            watch_directory(path, magic_word, extension, interval)
        except FileNotFoundError:
            logger.error(
                f'Directory or file not found: {os.path.abspath(path)}')

    logger.info(f"""
-------------------------------------------------------------------
    Stopped {__file__}
    Uptime was TODO: {'TODO'}
-------------------------------------------------------------------
    """)


if __name__ == '__main__':
    main(sys.argv[1:])
