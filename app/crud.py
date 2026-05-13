"""
This is the game logic layer (database operations)
"""

from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timedelta

def create_player(db: Session, email: str):
    player = models.Player(email=email)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def create_nation_with_city(db: Session, player_id, nation_name):
    nation = models.Nation(player_id=player_id, name=nation_name)
    db.add(nation)
    db.commit()
    db.refresh(nation)

    city = models.City(
        nation_id=nation.id,
        name="Capital",
        x=0,
        y=0
    )
    db.add(city)
    db.commit()
    db.refresh(city)

    resources = models.Resource(
        city_id=city.id,
        money=1000,
        food=500,
        oil=200,
        tech=50
    )
    db.add(resources)
    db.commit()

    return nation


def get_cities(db: Session, nation_id):
    return db.query(models.City).filter(models.City.nation_id == nation_id).all()


def get_resources(db, city_id):
    resource = db.query(models.Resource).filter(models.Resource.city_id == city_id).first()

    if not resource:
        return None 

    buildings = db.query(models.Building).filter(
        models.Building.city_id == city_id
    ).all()

    now = datetime.utcnow()
    elapsed = (now - resource.updated_at).total_seconds()

    # Basic production rates (per second)
    money_rate = 1
    food_rate = 0.5
    oil_rate = 0.2
    tech_rate = 0.1

    # Apply Building Bonsuses to production
    for b in buildings:
        if b.type == "farm":
            food_rate += 2 * b.level 
        elif b.type == "oil_rig":
            oil_rate += 1 * b.level
        elif b.type == "bank":
            money_rate += 2 * b.level
        elif b.type == "lab":
            tech_rate += 1 * b.level

    resource.money += int(elapsed * money_rate)
    resource.food += int(elapsed * food_rate)
    resource.oil += int(elapsed * oil_rate)
    resource.tech += int(elapsed * tech_rate)

    resource.updated_at = now

    db.commit()
    db.refresh(resource)

    return {
        "money": resource.money,
        "food": resource.food,
        "oil": resource.oil,
        "tech": resource.tech
    }


def start_build(db: Session, city_id: str, building_type: str):
    # Get building
    building = db.query(models.Building).filter(
        models.Building.city_id == city_id,
        models.Building.type == building_type
    ).first()

    if not building:
        building = models.Building(
            city_id=city_id,
            type=building_type,
            level=1
        )
        db.add(building)
        db.commit()
        db.refresh(building)

    next_level = building.level + 1

    # Simple cost formula
    cost = next_level * 200

    # get resources
    resource = db.query(models.Resource).filter(
        models.Resource.city_id == city_id
    ).first()

    if resource.money < cost:
        return {"error": "Not enough money"}

    resource.money -= cost

    # Time formula (scales per level)
    build_time = 30 * next_level # seconds

    queue_item = models.BuildQueue(
        city_id=city_id,
        building_type=building_type,
        target_level=next_level,
        started_at=datetime.utcnow(),
        completes_at=datetime.utcnow() + timedelta(seconds=build_time)
    )

    db.add(queue_item)
    db.commit()

    return {
        "message": "Build started",
        "building": building_type,
        "target_level": next_level,
        "completes_at": queue_item.completes_at
    }


def process_builds(db: Session, city_id: str):

    now = datetime.utcnow()

    queue_items = db.query(models.BuildQueue).filter(
        models.BuildQueue.city_id == city_id,
        models.BuildQueue.completes_at <= now
    ).all()

    for item in queue_items:

        building = db.query(models.Building).filter(
            models.Building.city_id == city_id,
            models.Building.type == item.building_type
        ).first()

        if building:
            building.level = item.target_level

        db.delete(item)

    db.commit()

    return {"message": f"Processed {len(queue_items)} builds"}

def get_buildings(db: Session, city_id: str):
    return db.query(models.Building).filter(
        models.Building.city_id == city_id
    ).all()

def get_build_queue(db: Session, city_id: str):
    return db.query(models.BuildQueue).filter(
        models.BuildQueue.city_id == city_id
    ).all()
