
from exceptions import FormException

class Form(object):
    def __init__(self, fields = {}):
        self.fields = fields

    def add_field(self, name, type):
        self.fields[name] = type


# add generate_form static function to the sqlalchemy.orm.Table classes
def as_form(orig_class):

    def gen(decorated_self, fields = []):

        form = Form(orig_class.__factory__.generate(decorated_self, fields))

        return form

    orig_class.generate_form = gen

    return orig_class
