#!/usr/bin/env python3

import sys

def usage():
    print('usage: html_gen [FILE]')
    sys.exit(1)

def get_lines():
    with open(sys.argv[1]) as f:
        lines = [line for line in f]

        for line in lines:
            yield line

def convert_text_to_html():
    ''' Write the text source into HTML markup '''

    with open('output.html', 'w') as out:
        with open(sys.argv[1]) as f:
            for line in get_lines():
                pass

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    convert_text_to_html()
