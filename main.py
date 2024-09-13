from fastapi import Depends,FastAPI,Body,Path, Query,Request
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel,Field
from typing import Optional,List
from utils.jwt_manager import create_token,validate_token
from routers.movie import movie_router
from routers.user import user_router
from config.database import Session,engine,Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer


app = FastAPI()
app.title = "Mi aplicacion con FastApi"
app.version = "0.0.1"


app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)



@app.get('/',tags=['home'])
def message():
    return HTMLResponse('<h1>Hello word</h1>')





