#!/usr/bin/env python
# encoding: utf-8

import web

import config
import os.path
from app.files import save_file, get_file

from lib.template import Render

urls = (
  '/',                             'index',
  '/robots\.txt',                  'robots',
  '/download/([a-zA-Z0-9]{6})/?',  'download',
  '/view/([a-zA-Z0-9]{6})/.*',     'view',
  '/([a-zA-Z0-9]{6})/?',           'upload',
)

app = web.application(urls, globals())

render = web.template.render('templates/', base='base', globals={'session': None})

render_plain = Render('templates/', base='plain', globals={'session': None})

class robots:
    def GET(self):
        return '''
User-agent: Googlebot
Disallow: /*

User-agent: Googlebot-Image
Disallow: /i/*
'''

class index:
    def GET(self):
        return render.index()

    def POST(self):
        x = web.input(file={}, key='')

        fo = x.file

        base = save_file(fo)

        return config.DOMAIN + base

class upload:
    def GET(self, base):
        f = get_file(base)
        if not f: return app.notfound()

        metafile = f.metafile()

        if metafile:
            return render_plain.render(metafile.template)(f, metafile)

        return render_plain.upload(f)

class download:
    def GET(self, base):
        f = get_file(base) 
        if not f: return app.notfound()

        web.header('Content-type', f.mime)
        web.header('Content-disposition', 'attachment; filename=' + f.name)
        data = ''
        with open(os.path.join(config.UPLOAD_DIRECTORY, f.filename)) as f:
            data = f.read()
        return data

class view:
    def GET(self, base):
        f = get_file(base)
        if not f: return app.notfound()

        if not f.type == 2: return app.notfound()

        metafile = f.metafile()

        web.header('Content-type', 'text/plain')
        return metafile.content 

if __name__ == '__main__':
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    application = app.wsgifunc()
    app.run()
