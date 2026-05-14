from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import ai,users
app = FastAPI()


app.add_middleware(CORSMiddleware,
                   allow_origins=["*"], # 允许所有源，开发阶段允许所有源
                   allow_credentials=True, # 允许携带cookie
                    allow_methods=["*"], # 允许所有方请求法
                    allow_headers=["*"],# 允许所有的请求头
                   )
app.include_router(users.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


