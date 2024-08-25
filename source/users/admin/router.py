from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from source.users.admin.services import add_user_role, delete_user_role, delete_user
from source.users.services.dependencies import check_admin_depend


router = APIRouter(
    prefix='/profile/_/_',
    tags=['Администрирование']
)


@router.get('/role/add', status_code=200)
async def add_role_router(user_id: PositiveInt, role: str,  admin_id = Depends(check_admin_depend)):
    return await add_user_role(user_id=user_id, role=role, admin_id=admin_id)

@router.delete('/role/delete', status_code=200)
async def delete_role_router(user_id: PositiveInt, role: str, admin_id = Depends(check_admin_depend)):
    return await delete_user_role(user_id=user_id, role=role)

@router.delete('/user', status_code=200)
async def delete_user_router(user_id: PositiveInt, admin_id = Depends(check_admin_depend)):
    return await delete_user(user_id=user_id, admin_id=admin_id)