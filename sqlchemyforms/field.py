
from abc import abstractmethod

import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy.orm.relationships import RelationshipProperty
from widget import Widget, SelectWidget

# ------------------------------------------------------------------------------------------------------------------------------------------------

# makes a connection between the ORM based classes and the HTML Form
class FieldBase(object):
    # custom keys for generate (HTML) fields
    __keys__ = [
        # TODO
        'represent',

        # TODO
        'widget',
    ]

    def __init__(self, kwargs):
        for key in self.__keys__:
            setattr(self, key, None)
            if key in kwargs:
                setattr(self, key, kwargs[key])
                # need to remove the custom keys from the kwargs before pass to the other parent's ctor
                kwargs.pop(key, None)


class Field(sqlalchemy.Column, FieldBase):

    def __init__(self, *args, **kwargs):
        FieldBase.__init__(self, kwargs)
        sqlalchemy.Column.__init__(self, *args, **kwargs)

class RelationshipField(RelationshipProperty, FieldBase):

    def __init__(self, *args, **kwargs):
        FieldBase.__init__(self, kwargs)
        RelationshipProperty.__init__(self, *args, **kwargs)

# ------------------------------------------------------------------------------------------------------------------------------------------------

class FieldDataProvider(object):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def get_data(self, widget):
        pass

class SelectFieldDataProvider(FieldDataProvider):

    def get_data(self, widget):

        # copy the fields to a new array
        fields = [widget.key_field]
        fields.extend(widget.value_fields)

        result = self.session.connection().execute(select(fields))

        options = {}

        for row in result:
            options[row[0]] = row

        return options

# ------------------------------------------------------------------------------------------------------------------------------------------------

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

        widget.multiple = True

        return widget

# ------------------------------------------------------------------------------------------------------------------------------------------------

class FieldFactory(object):
    __column_property_types__ = {
        sqlalchemy.orm.properties.ColumnProperty: SimpleFieldGenerator,
        RelationshipField: ManyToManyFieldGenerator
    }

    __providers__ = {
        Widget: FieldDataProvider,
        SelectWidget: SelectFieldDataProvider
    }

    def __init__(self, session):
        self.generators = {}
        self.providers = {}
        self.session = session

    def get_provider(self, type):
        if type not in self.providers:
            self.providers[type] = self.__providers__[type](self.session)
        return self.providers[type]

    def get_generator(self, type):
        if type not in self.generators:
            self.generators[type] = self.__column_property_types__[type]()

        return self.generators[type]

    def generate(self, table, fields = []):

        widgets = {}
        table_type = type(table)

        for name in dir(table_type):
            if len(fields) and name not in fields:
                continue

            attr = getattr(table_type, name)

            if type(attr) is not sqlalchemy.orm.attributes.InstrumentedAttribute:
                continue

            value = getattr(table, name)

            generator = self.get_generator(type(attr.property))
            widget = generator.get_widget(attr)

            if not widget:
                continue

            widget.setup(name, value, self.get_provider(type(widget)))
            widgets[name] = widget

        return widgets