#!/usr/bin/env python3

import sys
import re

def usage():
    print('usage: html_gen [FILE]')
    sys.exit(1)

def get_lines():
    with open(sys.argv[1]) as f:
        lines = [line for line in f]

        for line in lines:
            yield line

class Parser():
    def __init__(self):
        self.written_text = ''
        self.remaining_text = ''
        self.markup = { 'h1': '^[#]{1}(\s*)',
                        'h2': '^[#]{2}(\s*)',
                        'h3': '^[#]{3}(\s*)',
                        'h4': '^[#]{4}(\s*)',
                        'h5': '^[#]{5}(\s*)',
                        'h6': '^[#]{6}(\s*)',
                        'hr': '^-{3}',
                        'a': '(\[http(s?):\/{2}.+?\.(com|org|edu|net)\])'
                      }

    def get_tags(self):
        ''' Return the available markup symbols '''

        for tag in sorted(self.markup)[::-1]:
            yield tag

    def generate_tag(self, line):
        ''' Generate a tag

        Parameters:
          line: the line to generate HTML from
        '''

        return self.parse_line(line.replace('\n', ''))

    def parse_line(self, text):
        ''' Parse a line recursively for markup symbols

        Parameters:
          text: a textual line
        Returns: the generated HTML
        '''

        self.written_text = text
        self.remaining_text = ''

        for key in self.get_tags():
            if re.search(self.markup[key], text) and key == 'hr':
                self.written_text = '<hr>'
                break
            elif re.search(self.markup[key], text) and key != 'a':
                r = re.search(self.markup[key], text)
                self.remaining_text = text[r.span()[1]:]
                self.written_text = ''.join(['<', key, '>', self.parse_line(self.remaining_text),
                                       '</', key, '>\n'])
                self.remaining_text = ''
                break
            elif re.search(self.markup['a'], text):
                rng = re.search(self.markup['a'], text).span()
                linkname = text[rng[0] + 1: rng[1] - 1]

                # Check where the link is within the line
                if rng[0] > 0:
                    self.written_text = ''.join([text[:rng[0] - 1], " <a href='",
                                                 linkname, "'>", linkname, "</a> "])
                else:
                    self.written_text = ''.join(["<a href='", linkname, "'>",
                                                 linkname, "</a> "])

                self.remaining_text = text[rng[1] + 1:]

        if self.remaining_text == '':
            return self.written_text

        return self.written_text + self.parse_line(self.remaining_text)

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
