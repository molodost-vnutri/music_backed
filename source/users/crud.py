from sqlalchemy import select

from source.database import async_session
from source.Core import BaseCRUD
from source.users.models import UserModel, RoleModel, UserRoles
from source.users.schemes import SUserInformation

class RoleCRUD(BaseCRUD):
    model = RoleModel

class UserRolesCRUD(BaseCRUD):
    model = UserRoles

class UserCRUD(BaseCRUD):
    model = UserModel

    @classmethod
    async def model_get_current_user(cls, model_id: int):
        async with async_session() as session:
            query = (
                select(cls.model, RoleModel.role)
                .join(UserRoles, cls.model.id == UserRoles.user_id)
                .join(RoleModel, UserRoles.role_id == RoleModel.id)
                .filter(cls.model.id == model_id)
            )
            
            result = await session.execute(query)
            user_info = result.mappings().all()

            user = user_info[0][cls.model]
            roles = [row["role"] for row in user_info]

            return SUserInformation(
                username=user.username,
                email=user.email,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat(),
                roles=[role for role in roles]
            )