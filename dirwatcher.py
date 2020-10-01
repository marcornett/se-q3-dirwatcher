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


def create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s \n%(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return


def scan_single_file(single_file, path):
    with open(os.path.join(path, single_file)) as f:
        file_content = f.readlines()
        return (single_file, len(file_content))

    # with open(f'{path}/{filename}', 'r') as f:
    #     file_contents = f.read()
    #     print(file_contents)
    #     f.seek()
    # TODO return seek location


def detect_added_files(before, after):
    return [f for f in os.listdir(path)]


def detect_removed_files(file_dict):
    return []


before = {}


def watch_directory(path, magic_string, extension, interval):
    """Monitors given directory and reports back changes"""
    logger = create_logger()

    global before
    after = {f: 0 for f in os.listdir(path)}
    # add to before
    before.update(after)
    # check before to see if same as after
    print(before, after)
    after = detect_added_files()
    # added = [f for f in after if not f in before]
    # removed = [f for f in before if not f in after]
    # if added:
    #     print(added)
    # if removed:
    #     print(removed)
    # before = after

    # TODO Report new files that are added to your dictionary.
    # TODO For every entry in your dictionary, find out if it still exists in the directory. If not, remove it from your dictionary and report it as deleted.
    # update dict to have read the file at certain point and conditionally log new files that haven't been read yet

    # TODO Once you have synchronized your dictionary,
    # TODO it is time to iterate through all of its files and
    # TODO look for magic text, starting from the line number
    # TODO where you left off last time.
    # for f in file_dict:
    #     if f not in file_dict:
    #         print(f)
    #     else:
    #         file_dict.update(scan)
    #         print(file_dict)
    # # Scans files
    #     scan = scan_single_file(f, path)
    # return file_dict

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
    parser.add_argument('-ext', '--extension',
                        help='Extension type to look for.')
    parser.add_argument('-int', '--interval',
                        help='Polling interval. Default 1.0 seconds')
    parser.add_argument('magic', help='Magic text to search for')

    return parser


def signal_handler(sig_num, frame):
    """Handler for SIGTERM and SIGINT."""
    # uptime = datetime.datetime.now() - start_time
    logger = create_logger()
    logger.warning('Received ' + signal.Signals(sig_num).name)
    logger.info(f"""
-------------------------------------------------------------------
    Stopped {__file__}
    Uptime was TODO: {uptime}
-------------------------------------------------------------------
    """)
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
        parser.print_usage()
        sys.exit(1)
    path = ns.directory
    extension = ns.extension
    magic_word = ns.magic
    interval = ns.interval

    logger = create_logger()
    logger.info(f"""
-------------------------------------------------------------------
    Start {__file__}
-------------------------------------------------------------------
    """)

    start_time = datetime.datetime.now()

    #  TODO use exit flag
    # exit_flag = False
    while True:
        try:
            watch_directory(path, magic_word, extension, interval)
        except FileNotFoundError:
            logger.error(
                f'Directory or file not found: {os.path.abspath(path)}')
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
