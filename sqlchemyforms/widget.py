
from tools import Storage
from abc import abstractmethod

class Widget(Storage):
    def __init__(self, name, type, value = None):
        self.name = name
        self.type = type
        self.value = value
        self.iterable = ['name', 'type', 'value']

    def validate(self):
        return self.field.validate(self.value)

    def __iter__(self):
        for field in self.iterable:
            yield field

    def __repr__(self):
        return "<Widget(name=%(name)s, type=%(type)s, value=%(value)s)>" % self

class SelectWidget(Widget):
    html_type = 'select'

    def __init__(self, *args, **kwargs):
        super(SelectWidget, self).__init__(*args, **kwargs)
        self.multiple = False
        self.options = None
        self.iterable.extend(['multiple', 'options'])

    def __repr__(self):
        return "<SelectWidget(name=%(name)s, type=%(type)s, value=%(value)s, options=%(options)s, multiple=%(multiple)r)>" % self
