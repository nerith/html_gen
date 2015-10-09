# HTML_gen

HTML_gen is a HTML generator prototype that generates HTML using Markdown-like
text syntax. HTML_gen can currently generate headers, links, paragraphs, and
lists.

## Prerequisites

On Debian-based systems:
`sudo apt install python3 python3-nose`

## Usage

HTML_gen uses a Markdown-like syntax in source files to generate HTML output.

Currently, the following syntax is available:

```
# text (for h1 tag)
## text (for h2 tag)
### text (for h3 tag)
up to h6...

[link url](link text) to generate a link.

--- for hr tag
*text* for italic text
**text** for bold-faced text

* text for a list item
```

Additionally, the source file can be separated with whitespace to generate
paragraphs.

```
line1
line2

line3
line4
```

This will produce one paragraph consisting of line1 and line2 and another
paragraph consisting of line3 and line4.

Once a source file is available, run `python3 src/html_generator.py [input file]`
to generate HTML output.

Once the program is done running, the output will be in a default file
called `output.html`.

## Running tests

Tests are stored in the tests directory and depend on Python nose to run.
To run the tests, run `make test`.
