from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session  # type: ignore
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI(
    title='Fast do Zero',
    description='Aprenda FastAPI do zero, com exemplos práticos e didáticos.',
    version='0.0.1',
)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {
        'message': 'Olá Mundo!',
    }


def not_found_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with id {user_id} not found.',
        )
    return db_user


def permissions_same_user(current_id: int, userdb_id: int):
    if current_id != userdb_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )


# - - POST - -
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists.',
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists.',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )  # type: ignore

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    user_db = not_found_user(user_id, session)

    permissions_same_user(current_user.id, user_id)

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = get_password_hash(user.password)

    try:
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists.',
        )

    return user_db  # user -> request; user_db -> database


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    user_db = not_found_user(user_id, session)

    permissions_same_user(current_user.id, user_id)

    session.delete(user_db)
    session.commit()
    return {'message': 'User deleted successfully'}


# Exercio Aula 03 - GET /users/{user_id}
@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user_db = not_found_user(user_id, session)
    return user_db


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    # O OAuth2PasswordRequestForm tem os campos username e password,
    # por isso usamos ele aqui.
    user = session.scalar(select(User).where(User.email == form_data.username))
    breakpoint()
    # Se o usuário não existir, retornamos um erro 401.
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password.',
        )
    # Se a senha estiver incorreta, retornamos um erro 401.
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password.',
        )

    # Se tudo estiver correto, criamos um token de acesso.
    access_token = create_access_token(data={'sub': user.email})

    return {'token_type': 'Bearer', 'access_token': access_token}
