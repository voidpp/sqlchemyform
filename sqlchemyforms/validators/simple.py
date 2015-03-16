
from abc import abstractmethod

class SimpleValidator(object):

    def __init__(self, type):
        self.type = type

    @abstractmethod
    def check(self, value):
        return ''

    @abstractmethod
    def process_widget(self, widget, db):
        pass

    def format_value(self, value, field_type):
        return value