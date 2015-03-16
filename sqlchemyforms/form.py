
#from sqlchemyforms.sqlchemyforms.exceptions import FormException
from tools import Storage
from widget_factory import WidgetFactory

class Form(Storage):

    widget_factory = WidgetFactory()

    def __init__(self,
                 model,
                 db,
                 action,
                 method = 'POST',
                 fields = [],
                 name = ''):
        self.model = model
        self.db = db
        self.action = action
        self.method = method
        self.fields = fields
        self.name = name
        self.errors = {}

        self.widgets = []
        self.__widgets_by_name = {}
        self.iterables = ['name', 'action', 'method', 'widgets', 'errors']

    def __iter__(self):
        for field in self.iterables:
            yield field

    def generate_widgets(self, instance):
        self.widgets = self.widget_factory.generate(instance, self.model.form_field_definitions, self.db, self.fields)
        for widget in self.widgets:
            self.__widgets_by_name[widget.name] = widget

    def accept(self, data, instance):
        self.generate_widgets(instance)

        if data is None:
            return False

        data_fields = []

        for name in self.__widgets_by_name:
            if name in data:
                data_fields.append(name)

        if not len(data_fields):
            return False

        changed_fields = []

        for name in data_fields:
            widget = self.__widgets_by_name[name]

            # validate
            widget.value = data[name]
            errors = widget.validate()
            if len(errors):
                self.errors[name] = errors

            # check change
            value = getattr(instance, name)
            if value != widget.value:
                changed_fields.append(name)

        if len(self.errors):
            return False

        # update instance
        for name in data_fields:
            field = self.__widgets_by_name[name].field
            value = field.format_value(data[name])
            setattr(instance, name, value)

        self.db.add(instance)

        return True
