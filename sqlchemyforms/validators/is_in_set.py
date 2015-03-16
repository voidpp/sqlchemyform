
from simple import SimpleValidator
from sqlchemyforms.widget import SelectWidget

class IsInSetValidator(SimpleValidator):

    widget_type = SelectWidget

    def __init__(self, values, multiple = False):
        self.values = values
        self.multiple = multiple
        self._values = {}

    def check(self, value):
        if not self.multiple:
            value = [value]

        exists = self._values.keys()

        for val in value:
            if val not in exists:
                return 'value not in set'

        return ''

    def process_widget(self, widget, db):
        self.fetch_available_values(db)

        widget.options = self._values
        widget.multiple = self.multiple

    def fetch_available_values(self, db):
        self._values = self.values() if hasattr(self.values, '__call__') else self.values