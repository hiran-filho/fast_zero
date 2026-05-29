from fastapi import FastAPI

app = FastAPI(
    title='Fast do Zero',
    description='Aprenda FastAPI do zero, com exemplos práticos e didáticos.',
    version='0.0.1',
)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
