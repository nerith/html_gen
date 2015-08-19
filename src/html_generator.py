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
                        'a': '((\[https?:\/{2}.+?\.(com|org|edu|net)\])(\(.+?\)))'
                      }
        self.header = False
        self.in_paragraph = False
        self.previous_line = None

    def get_tags(self):
        ''' Return the available markup symbols '''

        for tag in sorted(self.markup)[::-1]:
            yield tag

    def generate_paragraph(self, text):
        ''' Check if a line starts or ends a paragraph

        A paragraph is currently determined by blank lines separating
        a block of text.
        '''

        if self.previous_line == '' and text != '' and not self.header:
            self.in_paragraph = True
            return_text = "<p>" + text
        elif self.previous_line != '' and text == '' and self.in_paragraph:
            self.in_paragraph = False
            return_text = "</p>\n"
        else:
            return_text = text

        self.previous_line = text

        return return_text

    def generate_tag(self, line):
        ''' Generate a tag

        Parameters:
          line: the line to generate HTML from
        '''

        self.header = False

        text = self.parse_line(line.replace('\n', ''))
        text = self.generate_paragraph(text)

        return text

    def parse_line(self, text):
        ''' Parse a line recursively for markup symbols

        Parameters:
          text: a textual line
        Returns: the generated HTML
        '''

        self.written_text = text
        self.remaining_text = ''

        for key in self.get_tags():
            match = re.search(self.markup[key], text)

            if match:
                if key == 'hr':
                    self.written_text = '<hr>'
                elif key != 'a':
                    self.remaining_text = text[match.span()[1]:]
                    self.written_text = ''.join(['<', key, '>', self.parse_line(self.remaining_text),
                                                 '</', key, '>\n'])
                    self.header = True
                elif key == 'a':
                    link_name = match.groups()[1].replace('[', '').replace(']', '')
                    link_title = match.groups()[3].replace('(', '').replace(')', '')

                    # Check where the link is within the line
                    if match.start(0) > 0:
                        self.written_text = ''.join([text[:match.start(0)], "<a href='",
                                                     link_name, "'>", link_title, "</a>"])
                    else:
                        self.written_text = ''.join(["<a href='", link_name, "'>",
                                                     link_title, "</a>"])

                    self.remaining_text = text[match.end(len(match.groups())):]

                break

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
