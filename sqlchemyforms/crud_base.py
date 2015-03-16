
from sf_exceptions import CrudException
from form import Form
from table.data_table import DataTable

class CrudRequest(object):
    def __init__(self, path, get, post, db):
        self.path = path
        self.get = get
        self.post = post
        self.db = db

class CrudBase(object):
    def __init__(self, model):
        self.model = model

    def search_primary_key(self):
        for field in self.model.form_field_definitions:
            if hasattr(field.type, 'primary_key') and field.type.primary_key:
                return field.type
        return None

    def __fetch_instance(self, request):
        primary_key_def = self.search_primary_key()

        if primary_key_def.key not in request.get:
            raise CrudException('%s is missing' % primary_key_def.key, 404)

        primary_value = request.get[primary_key_def.key][0]

        instance = request.db.query(self.model).filter_by(**{primary_key_def.key: primary_value}).first()

        if instance is None:
            raise CrudException('%s not found' % self.model, 404)

        return instance

    def do_create(self, request):
        instance = self.model()

        form = Form(self.model, request.db, request.path)

        form.accept(request.post.data, instance)

        return form

    def do_read(self, request):

        return self.__fetch_instance(request)

    def do_update(self, request):

        instance = self.__fetch_instance(request)

        form = Form(self.model, request.db, request.path)

        form.accept(request.post.data, instance)

        return form

    def do_delete(self, request):

        instance = self.__fetch_instance(request)

        request.db.delete(instance)

        return True

    def do_list(self, request):

        t = DataTable(self, request)

        return t.fetch()

