
import sqlalchemy
from sqlalchemy.orm.relationships import RelationshipProperty

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
