#!/usr/bin/env python
# encoding: utf-8

import web
from web.template import Template

class Render(web.template.Render):
    def render(self, name):
        t = self._template(name)
        if self._base and isinstance(t, Template):
            def template(*a, **kw):
                return self._base(t(*a, **kw))
            return template
        else:
            return self._template(name)
