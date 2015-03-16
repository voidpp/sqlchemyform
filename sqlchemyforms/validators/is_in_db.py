
from sqlalchemy.sql import select
from is_in_set import IsInSetValidator

from sqlalchemy.orm.relationships import RelationshipProperty

class IsInDBValidator(IsInSetValidator):

    def __init__(self, key_field, value_fields, multiple = False):
        self.key_field = key_field
        self.value_fields = value_fields
        self.multiple = multiple
        self._values = {}
        self._value_instances = {}

    def fetch_available_values(self, db):

        value_model = self.key_field.class_

        instances = db.query(value_model).all()

        options = {}

        for instance in instances:
            key_value = getattr(instance, self.key_field.key)
            options[key_value] = {val_field.key: getattr(instance, val_field.key) for val_field in self.value_fields}
            self._value_instances[key_value] = instance

        self._values = options

    def format_value(self, value, field_type):
        if type(field_type.property) is not RelationshipProperty:
            return value

        foreign_model = self.key_field.class_

        if not self.multiple:
            value = [value]

        instances = []

        for val in value:
            instances.append(self._value_instances[val])

        if self.multiple:
            return instances
        else:
            return instances[0]
