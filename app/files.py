#!/usr/bin/env python
# encoding: utf-8

import os.path
import re

import string
import random

import config

from lib import magic
from app.models import File, Image, Document, Audio

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, get_lexer_for_mimetype, guess_lexer, ClassNotFound, TextLexer

class DefaultFile(object):
    _split = re.compile(r'[\+%s]' % re.escape(''.join([os.path.sep, os.path.altsep or ''])))
    type = 0

    def _gen_base(self, length=6, uppercase=False):
        chars = string.ascii_lowercase + string.digits
        if uppercase:
            chars += string.ascii_uppercase
        return ''.join(random.choice(chars) for x in range(length))

    def _get_extension(self, filename):
        DOUBLE_EXTENSIONS = 'tar.gz', 'tar.bz2'

        base, ext = os.path.splitext(filename)
        if any([filename.endswith(x) for x in DOUBLE_EXTENSIONS]):
            base, first_ext = os.path.splitext(base)
            ext = first_ext + ext
        return ext

    def _secure_filename(self, path):
        return self._split.sub('', path)

    def __init__(self, f, mime_type):
        self.id       = 0
        self.f        = f
        self.mimetype = mime_type
        self.filename = self._secure_filename(self.f.filename)
        self.ext      = self._get_extension(self.filename)
        self.base     = self._gen_base()
        self.path     = os.path.join(config.UPLOAD_DIRECTORY, self.base + self.ext)

    def save(self):
        filename = self.f
        with open(self.path, 'wb') as f:
            f.write(self.f.value)

        if not self.id:
            entry = File()
            entry.name     = self.filename
            entry.type     = self.type
            entry.base     = self.base
            entry.filename = self.base + self.ext
            entry.size     = len(self.f.value)
            entry.mime     = self.mimetype

            entry.save()

            self.id = entry.id

        return self.base

class AudioFile(DefaultFile):
    type = 3

    def save(self):
        super(AudioFile, self).save()

        audio         = Audio()
        audio.file_id = self.id

        audio.save()

        return self.base

class TextFile(DefaultFile):
    type = 2

    def save(self):
        super(TextFile, self).save()

        lexer = None

        plain_ext = '.txt', '.log',

        if self.ext in plain_ext:
            lexer = TextLexer

        else:

            try:
                lexer = get_lexer_for_filename(self.filename)
            except ClassNotFound:
                try:
                    lexer = get_lexer_for_mimetype(self.mimetype)
                except ClassNotFound:
                    try:
                        lexer = guess_lexer(self.f.value)
                    except ClassNotFound:
                        lexer = TextLexer

        html = highlight(self.f.value, lexer, HtmlFormatter(linenos=True, lineanchors='line', anchorlinenos = True))

        txt = Document()

        txt.file_id = self.id
        txt.html    = html
        txt.content = self.f.value

        txt.save()

        return self.base

class ImageFile(DefaultFile):
    type = 1

    def save(self):
        super(ImageFile, self).save()
        img = Image()
        img.file_id = self.id
        img.image   = self.base + '.' + self.ext

        img.save()
        return self.base

FILE_TYPES = {
    'text':     TextFile,
    'image':    ImageFile,
    'audio':    AudioFile,
    'default':  DefaultFile,
}

def detect_file_type(fs):

    contents = fs.value
    mime = magic.from_buffer(contents, mime=True)

    type, sub_type = mime.split('/', 1)

    return FILE_TYPES.get(type, FILE_TYPES['default']), mime

def save_file(fs):
    obj, mime = detect_file_type(fs)

    f = obj(fs, mime)
    return f.save()
