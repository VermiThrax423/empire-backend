from datetime import datetime, timedelta
from .military_config import MILITARY
from . import models
from . import build_service


BASE_LOOT_PERCENT = 0.25
LOOTABLE_RESOURCES = ["money", "food", "oil", "tech"]

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

def resolve_combat(attacker_units, defender_units, defense_bonus=0):
    attack_power = calculate_power(attacker_units, "attack")
    defense_power = calculate_power(defender_units, "defense")
    defense_power *= (1 + defense_bonus)

    total = attack_power + defense_power

    if total == 0:
        return attacker_units, defender_units, {}, {}, "draw"
    
    attacker_loss_ratio = defense_power / total
    defender_loss_ratio = attack_power / total

    new_attacker = {}
    new_defender = {}

    attacker_losses = {}
    defender_losses = {}

    for unit, qty in attacker_units.items():
        remaining = int(qty * (1 - attacker_loss_ratio))
        new_attacker[unit] = remaining
        attacker_losses[unit] = qty - remaining

    for unit, qty in defender_units.items():
        remaining = int(qty * (1 - defender_loss_ratio))
        new_defender[unit] = remaining
        defender_losses[unit] = qty - remaining

    # Determine winner
    if sum(new_attacker.values()) > sum(new_defender.values()):
        winner = "attacker"
    elif sum(new_defender.values()) > sum(new_attacker.values()):
        winner = "defender"
    else:
        winner = "draw"

    win_ratio = attack_power / (attack_power + defense_power)

    return new_attacker, new_defender, attacker_losses, defender_losses, winner, win_ratio


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

        defense_bonus = build_service.get_defense_bonus(db, attack.defender_city_id)

        new_attacker, new_defender, attacker_losses, defender_losses, winner, win_ratio = resolve_combat(
            attacker_units,
            defender_units,
            defense_bonus
        )

        if winner == "attacker":
            if sum(defender_units.values()) == 0:
                attack.loot = {}
            else:
                loot = calculate_loot(db, attack.defender_city_id, win_ratio)

                attack.loot = loot
        else:
            attack.loot = {}

        resource = db.query(models.Resource).filter_by(
            city_id=attack.attacker_city_id
        ).first()

        for res, amount in attack.loot.items():
            setattr(resource, res, getattr(resource, res) + amount)

        report = models.BattleReport(
            attacker_city_id=attack.attacker_city_id,
            defender_city_id=attack.defender_city_id,

            attacker_units=attacker_units,
            defender_units=defender_units,

            attacker_losses=attacker_losses,
            defender_losses=defender_losses,

            winner=winner,

            loot=attack.loot
        )

        db.add(report)

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


def calculate_loot(db, defender_city_id, win_ratio):
    resource = db.query(models.Resource).filter_by(
        city_id=defender_city_id
    ).first()

    loot = {}

    for res in LOOTABLE_RESOURCES:

        amount = getattr(resource, res)

        stolen = int(amount * BASE_LOOT_PERCENT * win_ratio)

        loot[res] = stolen

        setattr(resource, res, amount - stolen)

    return loot