from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas, models
from .build_service import start_build, process_builds

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "API running"}


@app.post("/create-player")
def create_player(data: schemas.PlayerCreate, db: Session = Depends(get_db)):
    player = crud.create_player(db, data.email)
    nation = crud.create_nation_with_city(db, player.id, "New Nation")
    return {
        "player_id": str(player.id),
        "nation_id": str(nation.id)
    }


@app.get("/cities/{nation_id}")
def get_cities(nation_id: str, db: Session = Depends(get_db)):
    return crud.get_cities(db, nation_id)


@app.get("/resources/{city_id}")
def get_resources(city_id: str, db: Session = Depends(get_db)):
    return crud.get_resources(db, city_id)


@app.post("/build/{city_id}")
def build(city_id: str, building_type: str, db: Session = Depends(get_db)):
    return start_build(db, city_id, building_type)

@app.post("/process-builds/{city_id}")
def process(city_id: str, db: Session = Depends(get_db)):
    return process_builds(db, city_id)