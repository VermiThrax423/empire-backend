import math
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models
from .building_config import BUILDINGS


def get_building_level(db: Session, city_id, building_type):
    b = db.query(models.Building).filter_by(
        city_id=city_id,
        type=building_type
    ).first()
    return b.level if b else 0


def check_limit(db: Session, city_id, building_type):
    config = BUILDINGS[building_type]

    count = db.query(models.Building).filter_by(
        city_id=city_id,
        type=building_type
    ).count()

    return count < config["max_per_city"]


def get_cost(building_type, next_level):
    config = BUILDINGS[building_type]
    base = config["base_cost"]
    growth = config["growth_cost"]

    scaled_costs = {}

    for resource, amount in base.items():
        scaled_costs[resource] = int(amount * (growth ** (next_level - 1)))

    return scaled_costs


def has_enough_resources(resource, cost_dict):
    for res_type, amount in cost_dict.items():
        if getattr(resource, res_type) < amount:
            return False
    return True


def deduct_resources(resource, cost_dict):
    for res_type, amount in cost_dict.items():
        setattr(resource, res_type, getattr(resource, res_type) - amount)


def get_time(building_type, next_level):
    base = BUILDINGS[building_type]["base_time"]
    return int(base * (1 + 0.5 * (next_level - 1)))


def start_build(db: Session, city_id, building_type):
    config = BUILDINGS[building_type]

    if not check_limit(db, city_id, building_type):
        return {"error": "Building limit reached"}

    current_level = get_building_level(db, city_id, building_type)
    next_level = current_level + 1

    cost = get_cost(building_type, next_level)

    resource = db.query(models.Resource).filter_by(city_id=city_id).first()

    if not has_enough_resources(resource, cost):
        return {"error": "Not enough resources"}

    deduct_resources(resource, cost)

    build_time = get_time(building_type, next_level)

    queue = models.BuildQueue(
        city_id=city_id,
        building_type=building_type,
        target_level=next_level,
        started_at=datetime.utcnow(),
        completes_at=datetime.utcnow() + timedelta(seconds=build_time)
    )

    db.add(queue)
    db.commit()

    return {
        "message": "Build started",
        "building": building_type,
        "level": next_level,
        "cost": cost,
        "time": build_time
    }


def process_builds(db: Session, city_id):

    now = datetime.utcnow()

    queue_items = db.query(models.BuildQueue).filter(
        models.BuildQueue.city_id == city_id,
        models.BuildQueue.completes_at <= now
    ).all()

    for item in queue_items:

        building = db.query(models.Building).filter_by(
            city_id=city_id,
            type=item.building_type
        ).first()

        if not building:
            building = models.Building(
                city_id=city_id,
                type=item.building_type,
                level=0
            )
            db.add(building)

        building.level = item.target_level
        db.delete(item)

    db.commit()

    return {"processed": len(queue_items)}


def get_defense_bonus(db, city_id):
    buildings = db.query(models.Building).filter_by(city_id=city_id).all()

    total_bonus = 0

    for b in buildings:
        config = BUILDINGS.get(b.type)

        if not config:
            continue

        effects = config.get("effects", {})

        if "defense_bonus" in effects:
            total_bonus += effects["defense_bonus"] * b.level

    return total_bonus