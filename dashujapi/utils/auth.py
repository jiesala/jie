#整合根据Token查询用户，返回用户
from fastapi import Depends, HTTPException, Header

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users

async def get_current_user(authorization: str =Header(...,alias='Authorization'),
                           db: AsyncSession = Depends(get_db)):
    token=authorization.split(" ")[1]#获取token
    user=await users.get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="登录失效")
    return user



