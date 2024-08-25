from fastapi import APIRouter, Depends

from source.users.services.dependencies import check_current_depend
from source.users.crud import UserCRUD
from source.users.schemes import SBannedUser, SUnbannedUser, SChangePasswordModerator, SChangeEmailModerator
from source.users.moderation.services import banned_user, unbanned_user, change_password, change_email

router = APIRouter(
    prefix='/_/profile',
    tags=['Модерация пользователей']
)

@router.post('/ban', status_code=200)
async def banned_user_router(request: SBannedUser, moderator_id = Depends(check_current_depend)):
    return await banned_user(model_id=request.user_id, moderator_id=moderator_id)


@router.post('/unban', status_code=200)
async def unbanned_user_router(request: SUnbannedUser, moderator_id = Depends(check_current_depend)):
    return await unbanned_user(model_id=request.user_id, moderator_id=moderator_id)


@router.post('/change/password', status_code=200)
async def change_password_user_router(request: SChangePasswordModerator, _ = Depends(check_current_depend)):
    return await change_password(model_id=request.user_id)


@router.post('/change/email', status_code=200)
async def change_email_user_router(request: SChangeEmailModerator, _ = Depends(check_current_depend)):
    return await change_email(model_id=request.user_id, email=request.email)

@router.get('/all_users', status_code=200)
async def get_all_users_router(_ = Depends(check_current_depend)):
    return await UserCRUD.get_all_users()