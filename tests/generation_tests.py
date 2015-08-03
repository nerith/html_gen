#!/usr/bin/env python3
#
# Test HTML generation

import html_generator as html

def test_h1():
    assert(html.parse_line('# Header 1') == "<h1>Header 1</h1>\n")

def test_h2():
    assert(html.parse_line('## Header 2') == "<h2>Header 2</h2>\n")

def test_h3():
    assert(html.parse_line('### Header 3') == "<h3>Header 3</h3>\n")

def test_h4():
    assert(html.parse_line('#### Header 4') == "<h4>Header 4</h4>\n")

def test_h5():
    assert(html.parse_line('##### Header 5') == "<h5>Header 5</h5>\n")

def test_h6():
    assert(html.parse_line('###### Header 6') == "<h6>Header 6</h6>\n")
