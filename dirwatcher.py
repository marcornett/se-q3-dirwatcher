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


def search_for_magic(magic_string, line, file_name, line_num, path):
    """Searches a read line for a magic word and logs the file/line of word."""
    if magic_string in line:
        logger.info(
            f'Magic text found: line {line_num + 1} of file '
            f'{os.path.join(path, file_name)}')


def scan_single_file(file_dict, extension, path, magic_string):
    """Scans a file for extension and looks at each line of text"""
    for file_name in file_dict:
        with open(os.path.join(path, file_name)) as read_f:
            line_num = file_dict[file_name]
            lines = read_f.readlines()[line_num:]
            for line in lines:
                search_for_magic(magic_string, line,
                                 file_name, line_num, path)
                line_num += 1
                file_dict.update({file_name: line_num})


def detect_added_files(path, new_read, file_dict):
    """Logs added files to provided directory and adds them to global dict."""
    for f in new_read:
        if f not in file_dict:
            logger.info(f'Added {f}')
            file_dict.update({f: 0})


def detect_removed_files(path, new_read):
    """Logs removed files from provided directory and
    adds them to global dict."""
    global file_dict
    for f in list(file_dict):
        if f not in new_read:
            logger.info(f'Removed {f}')
            file_dict.pop(f)


def watch_directory(path, magic_string, extension, interval):
    """Monitors given directory and reports back changes"""
    global file_dict
    new_read = {f: 1 for f in os.listdir(path) if f.endswith(extension)}
    detect_added_files(path, new_read, file_dict)
    detect_removed_files(path, new_read)
    scan_single_file(file_dict, extension, path, magic_string)


def create_parser():
    """Creates command line parser object to accept one argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', '--directory', default='.',
                        help='Directory to watch.')
    parser.add_argument('-ext', '--extension', default='txt',
                        help='Extension type to look for.')
    parser.add_argument('-int', '--interval', type=int, default=1,
                        help='Polling interval. Default 1.0 seconds')
    parser.add_argument('magic', help='Magic text to search for')
    return parser


def signal_handler(sig_num, frame):
    """Handler for SIGTERM and SIGINT."""
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
        exit_flag = True
    path = ns.directory
    extension = ns.extension
    magic_word = ns.magic
    interval = ns.interval

    logger.info(f"""
-------------------------------------------------------------------
    Start {__file__}
-------------------------------------------------------------------
    """)
    start_time = datetime.datetime.now()
    global file_dict
    while not exit_flag:
        time.sleep(interval)
        try:
            watch_directory(path, magic_word, extension, interval)
        except FileNotFoundError:
            logger.error(
                f'Directory does not exist: {os.path.abspath(path)}')
            time.sleep(5)

    uptime = datetime.datetime.now() - start_time

    logger.info(f"""
-------------------------------------------------------------------
    Stopped {__file__}
    Uptime was TODO: {uptime}
-------------------------------------------------------------------
    """)


if __name__ == '__main__':
    main(sys.argv[1:])
