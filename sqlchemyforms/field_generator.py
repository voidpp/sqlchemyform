
import sqlalchemy

from widget import Widget, SelectWidget
from abc import abstractmethod

class FieldGenerator(object):
    @abstractmethod
    def get_widget(self, field):
        pass

class SimpleFieldGenerator(FieldGenerator):
    __basic_field_types__ = {
        sqlalchemy.Integer: 'integer',
        sqlalchemy.String: 'text',
        sqlalchemy.Text: 'text',
        sqlalchemy.DateTime: 'datetime',
        sqlalchemy.Boolean: 'checkbox'
    }

    def get_widget(self, field):
        if field.primary_key:
            return None

        if field.widget:
            widget = field.widget
        else:
            orm_type = type(field.type)
            html_type = self.__basic_field_types__[orm_type] if orm_type in self.__basic_field_types__ else 'text'
            widget = Widget(html_type)

        return widget

class ManyToManyFieldGenerator(FieldGenerator):

    def get_widget(self, field):

        widget = field.property.widget

        if not widget or type(widget) is not SelectWidget:
            raise Exception('no widget ManyToManyFieldGenerator')

        widget.data.multiple = True

        return widget
