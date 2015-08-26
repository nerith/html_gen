# HTML_gen

HTML_gen is a HTML generator prototype that generates HTML using Markdown-like
text syntax. HTML_gen can currently generate headers, links, and paragraphs.

## Prerequisites

On Debian-based systems:
`sudo apt install python3 python3-nose`

## Usage

Run `python3 src/html_generator.py [input file]` to generate HTML output.

Once the program is done running, the output will be in a default file
called `output.html`.

## Running tests

To run the tests, run `make test`.
