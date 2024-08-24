from sqlalchemy import select, insert
from pydantic import EmailStr

from source.exceptions import RollbackException
from source.database import async_session
from source.Core import BaseCRUD
from source.users.models import UserModel, RoleModel, UserRolesModel, UserMusicsModel
from source.users.schemes import SUserInformation

class UserMusicCRUD(BaseCRUD):
    model = UserMusicsModel

class RoleCRUD(BaseCRUD):
    model = RoleModel

class UserRolesCRUD(BaseCRUD):
    model = UserRolesModel

    @classmethod
    async def model_insert(cls, session, **arg):
        query = insert(cls.model).values(**arg).returning(cls.model.id)
        result = await session.execute(query)
        return result.scalar_one()

class UserCRUD(BaseCRUD):
    model = UserModel

    @classmethod
    async def model_insert(cls, session, **arg):
        query = insert(cls.model).values(**arg).returning(cls.model.id)
        result = await session.execute(query)
        return result.scalar_one()
        
    @classmethod
    async def model_get_current_user(cls, model_id: int):
        async with async_session() as session:
            query = (
                select(cls.model, RoleModel.role)
                .join(UserRolesModel, cls.model.id == UserRolesModel.user_id)
                .join(RoleModel, UserRolesModel.role_id == RoleModel.id)
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

    @classmethod
    async def create_user_with_role(cls, email: EmailStr, hash_password: str):
        async with async_session() as session:
            try:
                async with session.begin():
                    user_id = await cls.model_insert(
                        session=session,
                        email=email,
                        password=hash_password
                    )

                    await UserRolesCRUD.model_insert(
                        session=session,
                        user_id=user_id,
                        role_id=1
                    )
            except:
                raise RollbackException
