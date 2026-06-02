from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session  # type: ignore
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
    UserUpdate,
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


# - - POST - -
@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
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
        password=user.password,
    )  # type: ignore

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserUpdate
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):

    user_db = not_found_user(user_id, session)
    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password

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
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = not_found_user(user_id, session)
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
