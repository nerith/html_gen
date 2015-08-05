#!/usr/bin/env python3

import sys
import re

markup = { 'h1': '^[#]{1}(\s*)',
           'h2': '^[#]{2}(\s*)',
           'h3': '^[#]{3}(\s*)',
           'h4': '^[#]{4}(\s*)',
           'h5': '^[#]{5}(\s*)',
           'h6': '^[#]{6}(\s*)',
           'a': '(\[http(s?):\/{2}.+?(\.com|\.org|\.edu|\.net)\])'
         }

def usage():
    print('usage: html_gen [FILE]')
    sys.exit(1)

def get_lines():
    with open(sys.argv[1]) as f:
        lines = [line for line in f]

        for line in lines:
            yield line

def get_tags():
    ''' Return the available markup symbols '''

    for tag in sorted(markup)[::-1]:
        yield tag

def generate_tag(line):
    ''' Generate a tag

    Parameters:
      line: the line to generate HTML from
    '''

    return parse_line(line.replace('\n', ''))

def parse_line(text):
    ''' Parse a line recursively for markup symbols

    Parameters:
      text: a textual line
    Returns: the generated HTML
    '''

    written_text = text
    remaining_text = ''

    for key in get_tags():
        if re.search(markup[key], text) and key != 'a':
            r = re.search(markup[key], text)
            remaining_text = text[r.span()[1]:]
            written_text = ''.join(['<', key, '>', parse_line(remaining_text),
                                   '</', key, '>\n'])
            remaining_text = ''
            break
        elif re.search(markup['a'], text):
            rng = re.search(markup['a'], text).span()
            linkname = text[rng[0] + 1: rng[1] - 1]

            # Check where the link is within the line
            if rng[0] > 0:
                written_text = ''.join([text[:rng[0] - 1], " <a href='",
                                        linkname, "'>", linkname, "</a> "])
            else:
                written_text = ''.join(["<a href='", linkname, "'>",
                                        linkname, "</a> "])

            remaining_text = text[rng[1] + 1:]

    if remaining_text == '':
        return written_text

    return written_text + parse_line(remaining_text)

def write_html():
    ''' Writes the HTML '''

    html = '<!doctype HTML>\n<html>\n<head></head>\n<body>\n' + \
           str(convert_text_to_html()) + '\n</body>\n</html>'

    with open('output.html', 'w') as out:
        out.write(html)

def convert_text_to_html():
    ''' Converts the text source into HTML markup '''

    html = ''

    with open(sys.argv[1]) as f:
        for line in get_lines():
            html += generate_tag(line)

    return html

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    write_html()
