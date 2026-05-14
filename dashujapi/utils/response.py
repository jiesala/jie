from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(messsage:str='success',data=None):
    content={ "code":200,
             "message":messsage,
             "data":data
              }
    return JSONResponse(content=jsonable_encoder(content))