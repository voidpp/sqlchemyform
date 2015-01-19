
import sqlalchemy
from json import JSONEncoder

def orm_repr(orig_class):

    def _iter(self):
        for name in dir(orig_class):
            attr = getattr(orig_class, name)
            if type(attr) is not sqlalchemy.orm.attributes.InstrumentedAttribute:
                continue
            yield (name, getattr(self, name))

    def _repr(self):
        data = dict(self)
        return "<%s(%s)>" % (self.__class__.__name__, ', '.join(["%s=%s" % (name, data[name]) for name in data]))

    def _eq(self, other):
        if other is None:
            return False
        return dict(self) == dict(other)

    orig_class.__repr__ = _repr
    orig_class.__iter__ = _iter
    orig_class.__eq__ = _eq
    return orig_class


class JSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, '__iter__'):
            return dict(o)

        if hasattr(o, '__dict__'):
            return o.__dict__

        print o # FIXME: handle this case
        return None


# FIXME: move to the right place...!  (maybe sg like CompositeWidget...)
def check_composite_widget_struct(value, required):

    if type(value) is not dict or type(required) is not dict:
        return False

    def check_node(val_node, req_node):
        for key in req_node:
            if key not in val_node:
                return False

            if type(val_node[key]) is dict:
                if type(req_node[key]) is not dict:
                    return False

                if not check_node(val_node[key], req_node[key]):
                    return False

            elif type(val_node[key]) is not req_node[key]:
                return False

        return True

    return check_node(value, required)

