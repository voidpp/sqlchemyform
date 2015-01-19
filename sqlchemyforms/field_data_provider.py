
from sqlalchemy.sql import select
from abc import abstractmethod

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
