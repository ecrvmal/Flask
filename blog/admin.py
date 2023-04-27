from flask import redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import Admin, AdminIndexView, expose

from blog import models
from blog.extensions import db


class MyAdminIndexView(AdminIndexView):          # need is_staff rights to get to admin pg

    @expose("/")
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for("auth.login"))
        return super(MyAdminIndexView, self).index()


# Create admin with custom base template
admin = Admin(name="Blog Admin",
              index_view=MyAdminIndexView(),     # need is_staff rights to get to admin pg
              template_mode="bootstrap4")

# Add views


class CustomAdminView(ModelView):     # permission to edit models (can be used per model)

    def create_blueprint(self, admin):
        blueprint = super().create_blueprint(admin)
        blueprint.name = f'{blueprint.name}_admin'
        return blueprint

    def get_url(self, endpoint, **kwargs):
        if not (endpoint.startswith('.') or endpoint.startswith('admin.')):
            endpoint = endpoint.replace('.', '_admin.')
        return super().get_url(endpoint, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class TagAdminView(CustomAdminView):  # if (CustomAdminView) - need auth + staff
                                      # if (ModelView) - not need auth + staff
    column_searchable_list = ('name',)
    create_modal = True
    edit_modal = True


class ArticleAdminView(CustomAdminView):
    can_export = True
    export_types = ('csv', 'xlsx', )
    column_filters = ('author_id',)
    form_columns = ('title', 'text', 'author', 'tags', )
    column_searchable_list = ('title', 'text', )
    column_editable_list = ('title', 'text', 'author', 'tags', )


class AuthorAdminView(CustomAdminView):
    can_export = True
    export_types = ('csv', 'xlsx', )
    column_filters = ('user_id',)
    form_columns = ('id', 'user_id', )
    column_searchable_list = ('id', 'user_id', )
    column_editable_list = ('id', 'user_id', )


class UserAdminView(CustomAdminView):
    column_exclude_list = ('password',)
    column_details_exclude_list = ('password',)
    column_export_exclude_list = ('password',)
    form_columns = ('username', 'email', 'is_staff')
    can_delete = False
    can_edit = True
    can_create = False
    can_view_details = False
    column_editable_list = ('username', 'email', 'is_staff')


admin.add_view(ArticleAdminView(models.Article, db.session, category='Models'))
admin.add_view(TagAdminView(models.Tag, db.session, category='Models'))
admin.add_view(UserAdminView(models.User, db.session, category='Models'))
admin.add_view(AuthorAdminView(models.Author, db.session, category='Models'))



