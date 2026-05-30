from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (  # type: ignore
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(
    title='Fast do Zero',
    description='Aprenda FastAPI do zero, com exemplos práticos e didáticos.',
    version='0.0.1',
)

database = []


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {
        'message': 'Olá Mundo!',
    }


# @app.get(
#     '/exercicio-html', status_code=HTTPStatus.OK, response_class=HTMLResponse
# )
# def exercicio_aula_02():
#     return """
#     <html>
#       <head>
#         <title>Nosso olá mundo!</title>
#       </head>
#       <body>
#         <h1> Olá Mundo </h1>
#       </body>
#     </html>"""


# - - POST - -
@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Usuário com id {user_id} não encontrado.',
        )
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Usuário com id {user_id} não encontrado.',
        )

    return database.pop(user_id - 1)
