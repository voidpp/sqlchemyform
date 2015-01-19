
import sqlalchemy

from field_generator import SimpleFieldGenerator, ManyToManyFieldGenerator
from field_data_provider import FieldDataProvider, SelectFieldDataProvider
from field import RelationshipField

from widget import Widget, SelectWidget

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
        if type not in self.__column_property_types__:
            return None

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
            if generator is None:
                continue

            widget = generator.get_widget(attr)

            if not widget:
                continue

            widget.setup(name, value, self.get_provider(type(widget)))
            widgets[name] = widget

        return widgets