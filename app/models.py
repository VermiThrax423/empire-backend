from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from .database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Nation(Base):
    __tablename__ = "nations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    name = Column(String, nullable=False)


class City(Base):
    __tablename__ = "cities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nation_id = Column(UUID(as_uuid=True), ForeignKey("nations.id"))
    name = Column(String)
    x = Column(Integer)
    y = Column(Integer)


class Resource(Base):
    __tablename__ = "resources"

    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), primary_key=True)
    money = Column(BigInteger, default=0)
    food = Column(BigInteger, default=0)
    oil = Column(BigInteger, default=0)
    tech = Column(BigInteger, default=0)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Building(Base):
    __tablename__ = "buildings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False)

    type = Column(String, nullable=False)
    level = Column(Integer, default=1)


class BuildQueue(Base):
    __tablename__ = "build_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False)

    building_type = Column(String, nullable=False)
    target_level = Column(Integer, nullable=False)

    started_at = Column(TIMESTAMP, server_default=func.now())
    completes_at = Column(TIMESTAMP, nullable=False)


class Army(Base):
    __tablename__ = "army"

    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), primary_key=True)
    unit_type = Column(String, primary_key=True)
    quantity = Column(Integer, default = 0)


class TrainingQueue(Base):
    __tablename__ = "training_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"))

    unit_type = Column(String)
    quantity = Column(Integer)

    started_at = Column(TIMESTAMP, server_default=func.now())
    completes_at = Column(TIMESTAMP)


class Attack(Base):
    __tablename__ = "attacks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    attacker_city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"))
    defender_city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"))

    units = Column(JSONB)

    loot = Column(JSONB)

    departure_time = Column(TIMESTAMP, server_default=func.now())
    arrival_time = Column(TIMESTAMP)
    return_time = Column(TIMESTAMP)

    status = Column(String, default="traveling")


class BattleReport(Base):
    __tablename__ = "battle_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    attacker_city_id = Column(UUID(as_uuid=True))
    defender_city_id = Column(UUID(as_uuid=True))

    attacker_units = Column(JSONB)
    defender_units = Column(JSONB)

    attacker_losses = Column(JSONB)
    defender_losses = Column(JSONB)

    winner = Column(String)

    loot = Column(JSONB)

    created_at = Column(TIMESTAMP, server_default=func.now())
    