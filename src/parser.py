import re

class Parser:
    ''' The Parser class represents a parser that parses text using specified
    markup. Once the parser parses the text, HTML is generated as output.
    '''

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
                        'a': '((\[https?:\/{2}.+?\.(com|org|edu|net)\])(\(.+?\)))',
                        'b': '(\*).+?(\*)'
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
                elif key == 'b':
                    bolded_text = ''.join(["<", key, ">", text[match.end(1):match.start(2)], "</", key, ">"])

                    if match.start(0) > 0:
                        self.written_text = text[:match.start(0)] + bolded_text
                    else:
                        self.written_text = bolded_text

                    self.remaining_text = text[match.end(len(match.groups())):]
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
