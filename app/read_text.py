#!/usr/bin/env python2
# encoding: utf-8

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, get_lexer_for_mimetype, guess_lexer, ClassNotFound, TextLexer

contents = ''
with open('files.py') as f:
    contents = f.read()

lexer = None
try:
    lexer = get_lexer_for_filename('txt')
except ClassNotFound:
    try:
        lexer = get_lexer_for_mimetype('text/plain')
    except ClassNotFound:
        try:
            lexer = guess_lexer(contents)
        except ClassNotFound:
            lexer = TextLexer

hl_code = highlight(contents, lexer, HtmlFormatter(linenos=True, lineanchors='line', anchorlinenos = True))


