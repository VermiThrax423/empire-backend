from datetime import datetime, timedelta
from .military_config import MILITARY
from . import models


def train_units(db, city_id, unit_type, quantity):

    config = MILITARY[unit_type]

    # Check building requirements
    building = db.query(models.Building).filter_by(
        city_id=city_id,
        type=config["trained_in"]
    ).first()

    if not building or building.level < 1:
        return {"error": "Required building not available"}

    # Calculate cost
    total_cost = {}
    for res, amount in config["cost"].items():
        total_cost[res] = amount * quantity

    resource = db.query(models.Resource).filter_by(city_id=city_id).first()

    for res, amount in total_cost.items():
        if getattr(resource, res) < amount:
            return {"error": f"Not enough {res}"}

    # Deduct resources
    for res, amount in total_cost.items():
        setattr(resource, res, getattr(resource, res) - amount)

    # Calculate Training Time
    total_time = config["training_time"] * quantity

    queue = models.TrainingQueue(
        city_id=city_id,
        unit_type=unit_type,
        quantity=quantity,
        started_at = datetime.utcnow(),
        completes_at = datetime.utcnow() + timedelta(seconds=total_time)
    )

    db.add(queue)
    db.commit()

    return {
        "message": "Training started",
        "unit": unit_type,
        "quantity": quantity,
        "completes_at": queue.completes_at
    }


def process_training(db, city_id):
    now = datetime.utcnow()

    queue_items = db.query(models.TrainingQueue).filter(
        models.TrainingQueue.city_id == city_id,
        models.TrainingQueue.completes_at <= now
    ).all()

    for item in queue_items:

        army = db.query(models.Army).filter_by(
            city_id=city_id,
            unit_type=item.unit_type
        ).first()

        if not army:
            army = models.Army(
                city_id=city_id,
                unit_type=item.unit_type,
                quantity=0
            )
            db.add(army)

        army.quantity += item.quantity

        db.delete(item)

    db.commit()

    return {"processed": len(queue_items)}