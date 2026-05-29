from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message  # type: ignore

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


@app.get(
    '/exercicio-html', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
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
