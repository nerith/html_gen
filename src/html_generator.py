#!/usr/bin/env python3

import sys
from parser import Parser

def usage():
    print('usage: html_gen [FILE]')
    sys.exit(1)

def get_lines():
    with open(sys.argv[1]) as f:
        lines = [line for line in f]

        for line in lines:
            yield line

def write_html():
    ''' Writes the HTML '''

    html = '<!doctype HTML>\n<html>\n<head></head>\n<body>\n' + \
           str(convert_text_to_html()) + '\n</body>\n</html>'

    with open('output.html', 'w') as out:
        out.write(html)

def convert_text_to_html():
    ''' Converts the text source into HTML markup '''

    parser = Parser()
    html = ''

    with open(sys.argv[1]) as f:
        for line in get_lines():
            html += parser.generate_tag(line)

    return html

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    write_html()
