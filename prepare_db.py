#!/usr/bin/env python
# encoding: utf-8

import sys
from app import models
import sqlite3

try:
    from peewee import BaseModel
except:
    sys.exit('PeeWee not found. Exiting ..') 

if __name__ == '__main__':
    models.db.connect()
    for mod in dir(models):
        m = getattr(models, mod)
        if type(m) == BaseModel and mod != "BaseModel" and mod != "Model":
            try:
                m.create_table()
                print('Creating tables for: "%s"' % mod)
            except sqlite3.OperationalError:
                print('Tables for "%s" already exists, skipping ..' % mod)

    print('Done.')
