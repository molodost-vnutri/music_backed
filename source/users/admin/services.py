from source.users.crud import UserCRUD
from source.exceptions import RoleNotFoundException, UserNotFoundException, NotHavePermissionException
from source.users.schemes import SUserRoles

async def add_user_role(user_id: int, role: str, admin_id: int):
    if not SUserRoles.get(role.lower()):
        raise RoleNotFoundException
    if SUserRoles.get(role.lower()) == 3:
        raise NotHavePermissionException
    await UserCRUD.add_role(user_id=user_id, role_id=SUserRoles.get(role.lower()))
    return {
        'message': 'Роль с id {} role {} добавлена на аккаунт с id {}'.format(SUserRoles.get(role.lower()), role, user_id)
    }

async def delete_user_role(user_id: int, role: str):
    if not SUserRoles.get(role.lower()):
        raise RoleNotFoundException
    if SUserRoles.get(role.lower()) == 3:
        raise NotHavePermissionException
    await UserCRUD.delete_role(role_id=SUserRoles.get(role.lower()), user_id=user_id)
    return {
        'message': 'Роль {} успешно удалена у пользователя с id {}'.format(role, user_id)
    }

async def delete_user(user_id: int, admin_id: int):
    if admin_id == user_id:
        raise NotHavePermissionException
    user = await UserCRUD.model_find_one(id=user_id)
    if not user:
        raise UserNotFoundException
    await UserCRUD.model_delete(model_id=user_id)