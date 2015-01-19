
from abc import abstractmethod

class Data(object):
    pass

class Widget(object):
    def __init__(self, type = None):
        self.data = Data()
        self.data.type = type

    def setup(self, name, value, provider):
        self.data.name = name
        self.data.value = value

    def __iter__(self):
        for name in self.data.__dict__:
            yield (name, getattr(self.data, name))

    def __repr__(self):
        return "<Widget(name='%(name)s', type='%(type)s', value='%(value)s')>" % self.data.__dict__

class SelectWidget(Widget):
    def __init__(self, key_field, value_fields, multiple = False):
        super(SelectWidget, self).__init__(type = 'select')
        self.key_field = key_field
        self.value_fields = value_fields
        self.data.multiple = multiple

    def setup(self, name, value, provider):
        super(SelectWidget, self).setup(name, value, provider)
        self.data.options = provider.get_data(self)



