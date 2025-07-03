from pydantic import BaseModel, HttpUrl as Url, TypeAdapter
from datetime import date, datetime
from typing import Self


class BaseSchema(BaseModel):
    @classmethod
    # pega as colunas do banco de dados e instancia a classe
    def from_db(cls, args: tuple) -> Self:
        return cls(**{key: args[i] for i, key in enumerate(cls.__fields__.keys())})

    @classmethod
    # dado uma lista de modelos, ele retorna um json
    def models_to_json(cls, vals: list[Self]):
        return TypeAdapter(list[cls]).dump_python(vals, mode="json")


class User(BaseSchema):
    name: str
    email: str
    password: str
    user_type: str


class Team(BaseSchema):
    name: str
    emblem: Url
    total_matches: int
    total_points: int
    fouls: int
    team_yellow_cards: int
    team_red_cards: int
    wins: int
    draws: int
    losses: int
    goals: int
    own_goals: int


class Player(BaseSchema):
    name: str
    date_of_birth: date
    nationality: str
    photo: Url
    goals: int
    position: str
    shirt_number: int
    fouls: int
    yellow_cards: int
    red_cards: int
    team: str


class Coach(BaseSchema):
    name: str
    date_of_birth: date
    nationality: str
    photo: Url
    team_name: str


class Match(BaseSchema):
    id: int
    date_hour: datetime
    location: str
    home_team: str
    visitor_team: str
    home_goals: int
    visitor_goals: int


class Event(BaseSchema):
    id: int
    match_id: int
    date_hour: datetime
    player_number: int
    player_team: str
    event_type: str
