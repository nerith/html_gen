#!/usr/bin/env python3

import sys

def usage():
    print('usage: html_gen [FILE]')
    sys.exit(1)

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()
