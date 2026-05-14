from fastapi import APIRouter,HTTPException
from fastapi.openapi.utils import status_code_ranges
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from starlette import status

from models.user import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserChangePasswordRequest, UserUpdateRequest
from config.db_conf import get_db
from crud import users
from utils.response import success_response
from utils.auth import get_current_user

router=APIRouter(prefix='/api/hou',tags=['users'])

# 注册接口
@router.post('/register')
async def  register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    existing_user=await  users.get_user_by_username(db,user_data.name)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user = await users.create_user(db,user_data)
    token=await users.create_token(db,user.name_id)
    # return { "code":200,
    #          "message":"注册成功",
    #          "data":{"token":token,
    #                  "UserInfo":{
    #                     "username":user.name,
    #                     "id":user.name_id,
    #                  }
    #                  }}
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(messsage="注册成功",data=response_data)

# 登录接口
@router.post('/login')
async def login(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    user = await users.authenticate_user(db,user_data.name,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token=await users.create_token(db,user.name_id)
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(messsage="登录成功",data=response_data)

# 获取用户信息接口
@router.get('/info')
async def get_user_info(user=Depends(get_current_user)):
    return success_response(messsage="获取用户信息成功",data=UserRequest.model_validate( user,from_attributes= True))

# 修改用户信息接口
@router.put("/update")
async def update_user(user_data:UserUpdateRequest,
                      user:User=Depends(get_current_user),
                      db:AsyncSession=Depends(get_db)):
    user=await users.update_user(db,user,user_data.old_name,user_data.new_name)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户不存在")
    return success_response(messsage="更新用户信息成功")
#修改密码接口
@router.put("/password")
async def update_password(password_data:UserChangePasswordRequest,
                          user:User=Depends(get_current_user),
                          db:AsyncSession=Depends(get_db)):
    res_change=await users.change_password(db,user,password_data.old_password,password_data.new_password)
    if not res_change:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="密码错误")
    return success_response(messsage="修改密码成功")
# ai问答接口
@router.post("/ai")
async def ask_ai():
    pass

# 图表绘制接口
@router.get("/tubiao")
async def get_tubiao():
    pass