from fastapi import FastAPI

from .database import engine
from .utils import load_routers

app = FastAPI()

load_routers(app)
