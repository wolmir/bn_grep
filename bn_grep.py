#!/usr/bin/env python
import os
import re
import argparse


def pretty_print(content):
    print "   |---"
    for line in content.split('\n'):
        print '   | ' + line
    print "   |"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='The path to search.')
    parser.add_argument('-f', '--file-name-pattern',
        help="A regular expression to filter the filenames to be scanned.")
    # parser.add_argument('-nB', '--n-before',
    #     help='Number of characters before the ocurrence of pattern.',
    #     type=int)
    # parser.add_argument('-nA', '--n-after',
    #     help='Number of characters after the ocurrence of pattern.',
    #     type=int)
    parser.add_argument('-lB', '--l-before',
        help='Number of lines before the ocurrence of pattern.',
        type=int)
    parser.add_argument('-lA', '--l-after',
        help='Number of lines after the ocurrence of pattern.',
        type=int)
    parser.add_argument('regex', help='The expression to find.')
    return parser.parse_args()

def main():
    args = get_args()
    dir = '.'
    if args.path:
        dir = args.path
        print dir
    pattern = re.compile(args.regex)
    fname_pattern = re.compile(r".+")
    if args.file_name_pattern:
        fname_pattern = re.compile(args.file_name_pattern)
    lA, lB = 0, 0
    if args.l_before:
        lB = args.l_before
    if args.l_after:
        lA = args.l_after
    for root, dirs, files in os.walk(dir):
        for fname in files:
            if fname_pattern.match(fname):
                try:
                    file_path = os.path.join(root, fname)
                    with open(file_path, 'r') as source_file:
                        contents = source_file.read()
                        if pattern.search(contents):
                            print "--- " + file_path + ':'
                            content_lines = contents.split('\n')
                            for line_no in range(len(content_lines)):
                                if pattern.search(content_lines[line_no] + '\n'):
                                    start = max(line_no - lB, 0)
                                    end = min(line_no + lA, len(content_lines) - 1)
                                    line_nos = range(start, end)
                                    snippet = content_lines[start:end]
                                    snippet_with_line_nos = [str(x[0]) + ' ' + x[1] for x in zip(line_nos, snippet)]
                                    pretty_print('\n'.join(snippet_with_line_nos))
                            # re_matches = pattern.finditer(contents)
                            # for match in re_matches:
                            #     nb, na = 0, 0
                            #     if args.n_before:
                            #         nb = args.n_before
                            #     if args.n_after:
                            #         na = args.n_after
                            #     start = max(match.start() - nb, 0)
                            #     end = min(match.end() + na, len(contents) - 1)
                            #     substring = contents[start : end]
                            #     pretty_print(substring)
                except IOError as e:
                    print e


def print_exit_msg():
    print "\n\nEnd of Line.\n\n"
    print "                     <bn />"
    print "                Benito-Nemitz Inc."


def interruptable_program(func_name, interrupt_handler=None, exit_handler=None):
    try:
        func_name()
        if exit_handler:
            exit_handler()
    except KeyboardInterrupt as e:
        if interrupt_handler:
            interrupt_handler()
        else:
            print e


if __name__=='__main__':
    interruptable_program(main, print_exit_msg, print_exit_msg)