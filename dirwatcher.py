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


track_dict = {}


def watch_directory(path, magic_string, extension, interval):
    """Monitors given directory and reports back changes"""
    #  TODO Do synchronize your dictionary model with the actual directory contents
    files = []
    for r, d, f in os.walk(path):
        for filename in f:
            files.append(filename)

    # TODO For every file in the directory, add it to your dictionary if it is not already there(exclude files without proper extensions).
    for i, filename in enumerate(files):
        if extension in filename:
            if filename not in track_dict:
                track_dict[filename] = i
                # TODO report new files added to dictionary
            else:
                track_dict

    print(track_dict)

    with open(f'{path}/{filename}', 'r') as f:
        file_contents = f.readline()

    # TODO Do use a strategy of modeling the contents of the directory
    # TODO within your program using a dictionary. The keys will be filenames
    # TODO and the values will be the last line number that was read during
    # TODO the previous polling iteration. Keep track of the last line read.
    # TODO When opening and reading the file, skip over all the lines that
    # TODO you have previously examined.

    # TODO Do break up your code into small functions such as
    # TODO scan_single_file(), detect_added_files(),
    # TODO detect_removed_files(), and watch_directory().

    # TODO Report new files that are added to your dictionary.
    # TODO For every entry in your dictionary, find out if it still exists in the directory. If not, remove it from your dictionary and report it as deleted.
    # TODO Once you have synchronized your dictionary, it is time to iterate through all of its files and look for magic text, starting from the line number where you left off last time.


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
    """Handler for SIGTERM and SIGINT."""
    # All log messages should contain timestamps.

    # exceptions, magic text found events,
    # files added or removed from watched dir,
    # and OS signal events.
    logger = create_logger()
    logger.warning('Received ' + signal.Signals(sig_num).name)
    logger.info(f"""
-------------------------------------------------------------------
    Stopped dirwatcher.py
    Uptime was TODO: UPTIME
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
        # TODO find out if sys.exit is allowed here
        parser.print_usage()
        sys.exit(1)
    # path = os.path.abspath(ns.directory)
    path = ns.directory
    extension = ns.extension
    magic_word = ns.magic
    interval = ns.interval

    logger = create_logger()
    logger.info(f"""
-------------------------------------------------------------------
    Start dirwatcher.py
-------------------------------------------------------------------
    """)

    start_time = time.time()

    #  TODO use exit flag
    exit_flag = False
    while True:
        try:
            watch_directory(path, magic_word, extension, interval)
        except Exception:
            # TODO logging.error(f'Sorry but... {Exception}')
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
