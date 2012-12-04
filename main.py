#!/usr/bin/env python
# encoding: utf-8

import web

import config
import os.path
from app.files import save_file 
from app.models import File


urls = (
  '/', 'index',
  '/robots\.txt', 'robots',
  '/([a-zA-Z0-9]{6})(/raw|/download)?.*', 'upload',
)

app = web.application(urls, globals())

render = web.template.render('templates/', base='base', globals={'session': None})

render_plain = web.template.render('templates/')

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
    def GET(self, base, parameter):
        try:
            f = File.get(File.base == base)
        except File.DoesNotExist:
            return ''

        metafile = f.metafile()

        if parameter == '/download':

            web.header('Content-type', f.mime)
            web.header('Content-disposition', 'attachment; filename=' + f.name)
            data = ''
            with open(os.path.join(config.UPLOAD_DIRECTORY, f.filename)) as f:
                data = f.read()
            return data

        if parameter == '/raw' and f.type == 2:

            web.header('Content-type', 'text/plain')
            return metafile.content

        if metafile:
            return web.template.frender(config.TEMPLATES + metafile.template)(f, metafile)

        return render.upload(f)

if __name__ == '__main__':
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    #application = app.wsgifunc()
    app.run()
