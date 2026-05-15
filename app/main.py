from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas, models
from .build_service import start_build, process_builds
from .training_service import train_units, process_training
from .attack_service import send_attack, process_attacks
from fastapi.middleware.cors import CORSMiddleware
from .building_config import BUILDINGS


app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "*.app.github.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.get("/building-config")
def get_building_config():
    return BUILDINGS


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

@app.get("/buildings/{city_id}")
def get_buildings(city_id: str, db: Session = Depends(get_db)):
    return crud.get_buildings(db, city_id)

@app.get("/build-queue/{city_id}")
def get_build_queue(city_id: str, db: Session = Depends(get_db)):

    process_builds(db, city_id)

    return crud.get_build_queue(db, city_id)

@app.post("/train/{city_id}")
def train(city_id: str, unit_type: str, quantity: int, db: Session = Depends(get_db)):
    return train_units(db, city_id, unit_type, quantity)

@app.post("/process-training/{city_id}")
def process_training_api(city_id: str, db: Session = Depends(get_db)):
    return process_training(db, city_id)

@app.post("/attack")
def attack(attacker_city_id: str, defender_city_id: str, units: dict, db: Session = Depends(get_db)):
    return send_attack(db, attacker_city_id, defender_city_id, units)

@app.post("/process-attacks")
def process(db: Session = Depends(get_db)):
    return process_attacks(db)

@app.get("/battle-reports/{city_id}")
def get_reports(city_id: str, db: Session = Depends(get_db)):
    reports = db.query(models.BattleReport).filter(
        (models.BattleReport.attacker_city_id == city_id) | (models.BattleReport.defender_city_id == city_id)
    ).order_by(models.BattleReport.created_at.desc()).all()

    return reports
