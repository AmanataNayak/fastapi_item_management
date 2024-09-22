from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import item, user, auth, rating

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(item.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(rating.router)


@app.get('/')
def index():
    return {
        'message': 'Hello, World!'
    }
