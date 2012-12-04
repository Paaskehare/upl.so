#!/usr/bin/env python
# encoding: utf-8

import config

from peewee import *
import datetime

db = SqliteDatabase(config.DATABASE, threadlocals=True)
#db = SqliteDatabase('test.db')
#db = SqliteDatabase('/home/ole/Projects/webpy/uplso/test.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField()
    password = CharField()
    key      = CharField()

class File(BaseModel):
    template = 'upload.html'

    name     = CharField()
    user     = ForeignKeyField(User, related_name='files', null = True)
    base     = CharField(unique = True)
    filename = CharField(null = True)
    date     = DateTimeField(default = datetime.datetime.now)
    type     = IntegerField(default = 0)
    mime     = CharField(null=True)
    size     = IntegerField(default = 0)
    private  = BooleanField(default = False)

    def metafile(self):
        if not self.type: return None

        types = Image, Document, Audio

        metafile = None

        try:
            metafile = types[self.type - 1]
        except IndexError: return None

        return metafile.get(metafile.file_id == self.id)

class Image(BaseModel):
    template = 'image.html'
    file_id  = IntegerField(default=0)
    image    = CharField()

class Document(BaseModel):
    template = 'document.html'
    file_id  = IntegerField(default=0)
    html     = TextField(null = True)
    content  = TextField(null = True)

class Audio(BaseModel):
    template = 'audio.html'
    file_id  = IntegerField(default=0)

if __name__ == '__main__':
    db.connect()
    #User.create_table()
    #File.create_table()
    #Image.create_table()
    #Document.create_table()
    Audio.create_table()

    #f = File()

    #f.name = 'file.png'
    #f.base = 'qweqwa'
    #f.type = 1
    #f.save()

    #t = Image.create(name = 'file.png', image = 'yyy', file_id=f.id)

    #print(f.metafile())
