from pydantic import BaseModel

from datetime import datetime

from sqlalchemy import DateTime, Index
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String

class Base(DeclarativeBase):
    create_time=mapped_column(
        DateTime,
        default=datetime.now(),
        comment="创建时间")
    up_time=mapped_column(
        DateTime,
        default=datetime.now(),
        comment="更新时间")

class User(Base):
        __tablename__="user"

        __table_args__ = (
            Index("name_UNIQUE","name"),
        )

        name_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
        name:Mapped[str]=mapped_column(String(50),unique=True,nullable= False,comment="用户名")
        password:Mapped[str]=mapped_column(String(100),nullable= False,comment="密码")

    # 打印方法
        def __repr__(self):
            return f"User(name_id={self.name_id!r}, name={self.name!r}, password={self.password!r})"

class TokenBase(DeclarativeBase):
    pass
class Token(TokenBase):
    __tablename__="user_token"
    name_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    name:Mapped[str]=mapped_column(String(50),unique=True,nullable= False,comment="用户名")
    token:Mapped[str]=mapped_column(String(255),nullable= False,comment="token")
    expire_at:Mapped[datetime]=mapped_column(DateTime,nullable= False,comment="过期时间")
    create_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now(),comment="创建时间")

    def __repr__(self):
        return f"Token(name_id={self.name_id!r}, name={self.name!r}, token={self.token!r})"

class UserQuery(BaseModel):
    question: str
