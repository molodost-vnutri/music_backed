from datetime import datetime

from pydantic import EmailStr, PositiveInt
from sqlalchemy import text

from source.database import async_session
from source.users.schemes import SUserAuthOut, SUserModeratorOut
from source.Core import BaseCRUD
from source.users.models import UserModel
from source.exceptions import RollbackException, RoleNotFoundException, RoleAlreadyAddException

class UserCRUD(BaseCRUD):
    model = UserModel

    @classmethod
    async def model_insert(cls, email: EmailStr, hash_password: str):
        async with async_session() as session:
            try:
                async with session.begin():
                    result = await session.execute(
                        text('''
                            INSERT INTO users (email, password, created_at, updated_at, banned)
                            VALUES (:email, :password, :created_at, :updated_at, :banned)
                            RETURNING id
                        '''),
                        {
                            'email': email, 
                            'password': hash_password,
                            'created_at': datetime.now(),
                            'updated_at': datetime.now(),
                            'banned': False
                        })
                    user_id = result.scalar_one()

                    await session.execute(
                        text('''
                            INSERT INTO user_roles (user_id, role_id)
                            VALUES (:user_id, :role_id)
                        '''),
                        {'user_id': user_id, 'role_id': 1}
                    )
                    await session.commit()
            except Exception as e:
                await session.rollback()
                raise RollbackException

    @classmethod
    async def get_info_current_user(cls, model_id: PositiveInt):
        async with async_session() as session:
            query = text("""
                SELECT u.username, 
                       u.first_name,
                       u.last_name,
                       u.email, 
                       u.created_at, 
                       u.updated_at,
                       ARRAY_AGG(r.role) AS roles
                FROM users u
                LEFT JOIN user_roles ur ON u.id = ur.user_id
                LEFT JOIN roles r ON ur.role_id = r.id
                WHERE u.id = :user_id
                GROUP BY u.id, u.first_name, u.last_name;
            """)
            result = await session.execute(query, {'user_id': model_id})
            user_information = result.fetchall()
            user_data = [
                SUserAuthOut(
                    username=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    created_at=row[4].strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=row[5].strftime('%Y-%m-%d %H:%M:%S'),
                    roles=row[6],
                )
                for row in user_information
            ]
            return user_data[0]
    

    @classmethod
    async def get_all_roles_id(cls, model_id: PositiveInt):
        async with async_session() as session:
            query =  text('''
                SELECT array_agg(json_build_array(ur.role_id, r.role)) AS role_ids
                FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id
                WHERE ur.user_id = :user_id;
            ''')
            result = await session.execute(query, {'user_id': model_id})
            return result.mappings().fetchall()
        
    @staticmethod
    async def get_all_users():
        async with async_session() as session:
            query = text('''
                SELECT
                   id,
                   email,
                   username,
                   first_name,
                   last_name,
                   created_at,
                   updated_at,
                   banned
                FROM users
            ''')
            result = await session.execute(query)
            rows = result.fetchall()
            users_list = [
                SUserModeratorOut(
                    id=row[0],
                    email=row[1],
                    username=row[2],
                    first_name=row[3],
                    last_name=row[4],
                    created_at=row[5].strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=row[6].strftime('%Y-%m-%d %H:%M:%S'),
                    banned=row[7]
                )
                for row in rows
            ]

            return users_list
    
    @staticmethod
    async def get_all_roles():
        async with async_session() as session:
            query = text('''
                        SELECT id, role
                        FROM roles
                         ''')
            result = await session.execute(query)
            return [(role[0], role[1]) for role in result.fetchall()]
    
    @staticmethod
    async def add_role(user_id: int, role_id: int):
        async with async_session() as session:
            query = text('''SELECT (user_id, role_id)
                         FROM user_roles
                         WHERE user_id = :user_id
                         AND role_id = :role_id
                         ''')
            exist = await session.execute(query, {'user_id': user_id, 'role_id': role_id})
            result = exist.scalar_one_or_none()
            if result:
                raise RoleAlreadyAddException
            query = text('''INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id);''')
            await session.execute(query, {'user_id': user_id, 'role_id': role_id})
            await session.commit()
    
    @staticmethod
    async def delete_role(user_id: int, role_id: int):
        async with async_session() as session:
            query = text('''
            SELECT (user_id, role_id)
            FROM user_roles
            WHERE user_id = :user_id
            AND role_id = :role_id
            ''')
            result = await session.execute(query, {'user_id': user_id, 'role_id': role_id})
            exist = result.scalar_one_or_none()
            if not exist:
                raise RoleNotFoundException
            query = text('''
                DELETE FROM user_roles
                WHERE user_id = :user_id
                AND role_id = :role_id
            ''')
            await session.execute(query, {'user_id': user_id, 'role_id': role_id})
            await session.commit()