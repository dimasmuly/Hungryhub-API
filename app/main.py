from fastapi import FastAPI

from app.database import Base, engine
from app.initial_data import seed_data
from app.routers import restaurants, menu_items


app = FastAPI(title="HungryHub Restaurant Menu Management API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_data()


app.include_router(restaurants.router)
app.include_router(menu_items.router)
