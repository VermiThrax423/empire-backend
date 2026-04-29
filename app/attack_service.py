from datetime import datetime, timedelta
from .military_config import MILITARY
from . import models


def get_slowest_speed(units, military_config):
    speeds = []
    for unit_type, qty in units.items():
        if qty > 0:
            speeds.append(military_config[unit_type]["speed"])
    return min(speeds) if speeds else 1

def calculate_distance(city_a, city_b):
    return 10 # placeholder until add coordinates

def calculate_travel_time(units):
    distance = 10 # Placeholder until we add coordinates
    slowest = get_slowest_speed(units, MILITARY)

    return int(distance / slowest * 10) # scaled for gameplay

def send_attack(db, attacker_city_id, defender_city_id, units):
    # Check player has units
    for unit_type, qty in units.items():
        army = db.query(models.Army).filter_by(
            city_id=attacker_city_id,
            unit_type=unit_type
        ).first()

        if not army or army.quantity < qty:
            return {"error": f"Not enough {unit_type}"}
        
    # Deduct units
    for unit_type, qty in units.items():
        army = db.query(models.Army).filter_by(
            city_id=attacker_city_id,
            unit_type=unit_type
        ).first()

        army.quantity -= qty

    travel_time = calculate_travel_time(units)

    attack = models.Attack(
        attacker_city_id=attacker_city_id,
        defender_city_id=defender_city_id,
        units=units,
        arrival_time=datetime.utcnow() + timedelta(seconds=travel_time),
        return_time=datetime.utcnow() + timedelta(seconds=travel_time * 2),
        status="traveling"
    )

    db.add(attack)
    db.commit()

    return {
        "message": "Attack sent",
        "arrival_time": attack.arrival_time
    }

def calculate_power(units, stat):
    total = 0
    for unit_type, qty in units.items():
        total += qty * MILITARY[unit_type][stat]
    return total

def resolve_combat(attacker_units, defender_units):
    attack_power = calculate_power(attacker_units, "attack")
    defense_power = calculate_power(defender_units, "defense")

    total = attack_power + defense_power

    if total == 0:
        return attacker_units, defender_units
    
    attacker_loss_ratio = defense_power / total
    defender_loss_ratio = attack_power / total

    # Apply losses
    for unit in attacker_units:
        attacker_units[unit] = int(attacker_units[unit] * (1 - attacker_loss_ratio))

    for unit in defender_units:
        defender_units[unit] = int(defender_units[unit] * (1 - defender_loss_ratio))

    return attacker_units, defender_units

def process_attacks(db):

    now = datetime.utcnow()

    arrivals = db.query(models.Attack).filter(
        models.Attack.arrival_time <= now,
        models.Attack.status == "traveling"
    ).all()

    for attack in arrivals:

        defender_army = db.query(models.Army).filter_by(
            city_id=attack.defender_city_id
        ).all()

        defender_units = {
            a.unit_type: a.quantity for a in defender_army
        }

        attacker_units = attack.units

        new_attacker, new_defender = resolve_combat(
            attacker_units,
            defender_units
        )

        # Update defender army
        for unit_type, qty in new_defender.items():
            army = db.query(models.Army).filter_by(
                city_id=attack.defender_city_id,
                unit_type=unit_type
            ).first()

            if army:
                army.quantity = qty

        # Save survivors for return trip
        attack.units = new_attacker
        attack.status = "returning"

    # Handle Return units
    returns = db.query(models.Attack).filter(
        models.Attack.return_time <= now,
        models.Attack.status == "returning"
    ).all()

    for attack in returns:

        for unit_type, qty in attack.units.items():
            if qty <= 0:
                continue

            army = db.query(models.Army).filter_by(
                city_id=attack.attacker_city_id,
                unit_type=unit_type
            ).first()
            
            if not army:
                army = models.Army(
                    city_id=attack.attacker_city_id,
                    unit_type=unit_type,
                    quantity=0
                )
                db.add(army)

            army.quantity += qty

        # Mark attack complete (or delete)
        attack.status = "completed"

        # Optional: delete instead
        # db.delete(attack)

    db.commit()

    return {
        "arrivals_processed": len(arrivals),
        "returns_processed": len(returns)
    }