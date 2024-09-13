from fastapi import Depends,Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Optional,List
from config.database import Session

from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieServices

from fastapi import APIRouter
from schemas.movie import Movie
from models.movie import Movie as MovieModel



movie_router = APIRouter()


@movie_router.get('/movies',tags=['movies'],response_model=List[Movie], status_code=200,dependencies=[Depends(JWTBearer)])
def getMovies() -> List[Movie]: 
    db = Session()
    result= MovieServices(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}',tags=['movies'],response_model=Movie)
def get_movie(id:int= Path(ge=1,le=2000)) -> Movie:
    db = Session()
    result = MovieServices(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={"message", "No encontrado"})
    
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
    

@movie_router.get('/movies/',tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category: str=Query(min_length=5,max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieServices(db).get_movies_by_category(category)
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def createMovies(movie:Movie) -> dict:
    db = Session()
    MovieServices(db).create_Movie(movie)
    movies.append(movie)
    return JSONResponse(status_code=201,content={"message": "Se registro la pelicula"})


@movie_router.put('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def updateMovie(id:int,movie:Movie) -> dict :
    db = Session()
    result = MovieServices(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={"message": "No encontrado"})
    MovieServices(db).update_movie(id,movie)
    return JSONResponse(status_code=200,content={"message": "Se ha modificado la  pelicula"})
            

@movie_router.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def delete_Movie(id:int) -> dict:
    db = Session()
    result:MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404,content={"message": "No encontrado"})
    MovieServices(db).delete_movie(id)
    return JSONResponse(status_code=200,content={"message": "Se ha eliminado la pelicula"})
            