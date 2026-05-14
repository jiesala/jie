from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    name:str
    password:str
    model_config = ConfigDict(
        from_attributes=True,   #允许从ORM对象中获取字段
    )

class UserInfoResponse(BaseModel):
    name_id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,   #允许从ORM对象中获取字段
    )

class UserAuthResponse(BaseModel):
    token: str
    user_info:UserInfoResponse=Field(...,alias="UserInfo")

    model_config = ConfigDict(
        populate_by_name=True,  #alias/字段名兼容
        from_attributes=True,   #允许从ORM对象中获取字段
    )



class UserUpdateRequest(BaseModel):
    old_name: str=Field(...,alias="oldName")
    new_name: str=Field(...,alias="newName")
    model_config = ConfigDict(
        from_attributes=True,   #允许从ORM对象中获取字段
    )

class UserChangePasswordRequest(BaseModel):
    old_password: str=Field(...,alias="oldPassword")
    new_password: str=Field(...,alias="newPassword")
    model_config = ConfigDict(
        from_attributes=True,   #允许从ORM对象中获取字段
    )
