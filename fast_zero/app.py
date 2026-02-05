from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()


database = []


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
  user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
  database.append(user_with_id)

  return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}


@app.get('/exercicio-html', response_class=HTMLResponse)
def exercicio_aula_02():
    return """
    <html>
      <head>
        <title>Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""

# @app.post('/users/' , status_code=HTTPStatus.CREATED)
# def create_user(user: UserSchema):
#     return user


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    return user


@app.get('/users/', response_model=UserList)
def read_users():
  return {'users': database}


# @app.get('/', response_class=HTMLResponse)
# def hello():
#         return """
#     <html>
#       <head>
#         <title> Nosso olá mundo!</title>
#       </head>
#       <body>
#         <h1> Olá Mundo </h1>
#       </body>
#     </html>"""


# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pathlib import Path

# app = FastAPI()

# # Diretório contendo arquivos estáticos
# BASE_DIR = Path(__file__).parent
# app.mount('/static', StaticFiles(directory=BASE_DIR / 'static'), name='static')

# # Diretório contendo os templates Jinja
# templates = Jinja2Templates(directory=BASE_DIR / 'templates')


# @app.get('/{nome}', response_class=HTMLResponse)
# def home(request: Request, nome: str):
#     return templates.TemplateResponse(
#         request=request, name='index.html', context={'nome': nome}
#     )
