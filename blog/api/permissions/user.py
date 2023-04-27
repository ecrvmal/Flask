from combojsonapi.permission import PermissionMixin, PermissionForGet, PermissionForPatch, PermissionUser
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user


class UserListPermission(PermissionMixin):
    ALL_AVAILABLE_FIELDS = (
        'id',
        'username',
        'is_staff',
    )

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:
        if not current_user.is_authenticated:
            raise AccessDenied('No Access')
        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS,10)
        return self.permission_for_get


class UserPatchPermission(PermissionMixin):
    """Describe permission for patch User.
    Example request:
    curl --location --request PATCH 'http://127.0.0.1:5000/api/users/1' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "data": {
        "type": "user",
        "id": 1,
        "attributes": {
          "first_name": "John",
          "last_name": "Smith",
          "email": "john.smith@example.com"
        }
      }
    }'
    """

    PATCH_AVAILABLE_FIELSD =(
        'username',
        'email',
    )

    def patch_permission (self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELSD, 10)
        return self.permission_for_patch

    def patch_data(self, *args, data=None, obj=None, user_permission: PermissionUser = None, **kwargs) -> dict:

        # returns dict - for object update
        # data = input data, validated
        # obj = обновляемые данные from  DB
        # user permission - limit of rights
        # applicable to selected model
        permission_for_patch = user_permission.permission_for_patch_permission(model=User)
        return {
            k: v
            for k, v in data.items()
            if k in permission_for_patch.columns
        }