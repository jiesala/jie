import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from starlette import status

from models.user import User, Token
from schemas.users import UserRequest
from utils import security
from utils.security import  get_hash_password


# 通过用户名查询用户
async def get_user_by_username(db: AsyncSession, username:str):
    query_user=select(User).where(User.name==username)
    result =await db.execute(query_user)
    return result.scalar_one_or_none()
# 创建用户
async def create_user(db: AsyncSession, user_data:UserRequest):
    hass_password=get_hash_password(user_data.password)
    new_user=User(name=user_data.name,password=hass_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
# 创建token
async def create_token(db: AsyncSession, name_id:int):
    token= str(uuid.uuid4())
    expire_at=datetime.now() + timedelta(days=7)
    query=select(Token).where(Token.name_id==name_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expire_at=expire_at
    else:
        new_token=Token(name_id=name_id,token=token,expire_at=expire_at)
        db.add(new_token)
        await db.commit()

    return token
# 认证用户
async def authenticate_user(db: AsyncSession, username:str,password:str):
    user=await get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password,user.password):
        return None
    return user
# 通过token查询用户
async def get_user_by_token(db: AsyncSession, token:str):
    query=select(Token).where(Token.token==token)
    result=await db.execute(query)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expire_at < datetime.now():
        return None
    query_user=select(User).where(User.name_id==db_token.name_id)
    result=await db.execute(query_user)
    return result.scalar_one_or_none()

# 更新用户
async def update_user(db: AsyncSession, user:User, old_user_name:str,new_user_name:str,):
    if  old_user_name != user.name:
        return False
    user.name= new_user_name
    db.add(user)  # 更新数据库,由sqlalchemy真正接管user对象，确保可以提交。
    await db.commit()
    await db.refresh(user)
    return True
# 修改密码
async def change_password(db: AsyncSession,user:User, old_password:str,new_password:str):
    if not security.verify_password(old_password,user.password):
        return  False
    user.password=security.get_hash_password(new_password)
    db.add(user)  # 更新数据库,由sqlalchemy真正接管user对象，确保可以提交。
    await db.commit()
    await db.refresh(user)
    return True


