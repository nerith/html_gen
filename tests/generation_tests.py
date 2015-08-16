#!/usr/bin/env python3
#
# Test HTML generation

from nose.tools import assert_equals
from html_generator import Parser

parser = Parser()

def test_h1():
    assert_equals(parser.parse_line('# Header 1'), "<h1>Header 1</h1>\n")

def test_h2():
    assert_equals(parser.parse_line('## Header 2'), "<h2>Header 2</h2>\n")

def test_h3():
    assert_equals(parser.parse_line('### Header 3'), "<h3>Header 3</h3>\n")

def test_h4():
    assert_equals(parser.parse_line('#### Header 4'), "<h4>Header 4</h4>\n")

def test_h5():
    assert_equals(parser.parse_line('##### Header 5'), "<h5>Header 5</h5>\n")

def test_h6():
    assert_equals(parser.parse_line('###### Header 6'), "<h6>Header 6</h6>\n")

def test_hr():
    assert_equals(parser.parse_line('---'), "<hr>")

def test_start_link_generation():
    assert_equals(parser.parse_line('[https://www.google.com](Google)'),
                  "<a href='https://www.google.com'>Google</a>")

    assert_equals(parser.parse_line('[https://www.google.com](Google) is a link'),
                  "<a href='https://www.google.com'>Google</a> is a link")

def test_embedded_link_generation():
    assert_equals(parser.parse_line('This is a link -> [https://www.google.com](Google) to Google'),
                  "This is a link -> <a href='https://www.google.com'>Google</a> to Google")

def test_paragraph_generation():
    parser.generate_tag('')

    assert_equals(parser.generate_tag("This is a paragraph"), "<p>This is a paragraph")
    assert_equals(parser.generate_tag("Second line of the paragraph"), "Second line of the paragraph")
    assert_equals(parser.generate_tag(''), "</p>\n")

    parser.generate_tag('')

    assert_equals(parser.generate_tag('A line with a link > [https://www.google.com](Google)'),
                  "<p>A line with a link > <a href='https://www.google.com'>Google</a>")
    assert_equals(parser.generate_tag(''), "</p>\n")
