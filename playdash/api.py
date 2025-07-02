from flask import Request
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_openapi3.blueprint import APIBlueprint

from playdash.db import get_db
from playdash.schema import User, Team, Player, Coach, Match, Event
import json

from pydantic import RootModel, BaseModel


class PathID(BaseModel):
    id: int


class PathName(BaseModel):
    name: str


bp = APIBlueprint("api", __name__, url_prefix="/api")
user_tag = Tag(name="user")
team_tag = Tag(name="team")
player_tag = Tag(name="player")
coach_tag = Tag(name="coach")
match_tag = Tag(name="match")
event_tag = Tag(name="event")


@bp.get(
    "/user",
    summary="return all users",
    tags=[user_tag],
    responses={200: RootModel[list[User]]},
)
def get_all_users() -> list[User]:
    db = get_db()
    users = db.execute("SELECT * FROM usuario ").fetchall()
    return User.models_to_json([User.from_db(val) for val in users])


@bp.get(
    "/user/<name>",
    summary="return one specific user",
    tags=[user_tag],
    responses={200: RootModel[list[User]]},
)
def get_one_user(path: PathName):
    db = get_db()
    user = db.execute(
        "SELECT * FROM usuario WHERE nome_usuario=?", [path.name]
    ).fetchone()
    return User.models_to_json(User.from_db(user))


@bp.post("/user/")
def create_user(request: Request):
    data = User(**request.json)
    db.execute("insert into ")


@bp.get(
    "/team",
    summary="return all teams",
    tags=[team_tag],
    responses={200: RootModel[list[Team]]},
)
def get_all_teams() -> list[Team]:
    db = get_db()
    teams = db.execute("SELECT * FROM 'time' ").fetchall()
    return Team.models_to_json([Team.from_db(val) for val in teams])


@bp.get(
    "/team/<name>",
    summary="return one specific team",
    tags=[team_tag],
    responses={200: RootModel[list[Team]]},
)
def get_one_team(path: PathName):
    db = get_db()
    team = db.execute("SELECT * FROM 'time' WHERE nome_time=?", [path.name]).fetchone()
    return Team.models_to_json(Team.from_db(team))


@bp.get(
    "/player",
    summary="return all players",
    tags=[player_tag],
    responses={200: RootModel[list[Player]]},
)
def get_all_players() -> list[Player]:
    db = get_db()
    players = db.execute("SELECT * FROM jogador ").fetchall()
    return Player.models_to_json([Player.from_db(val) for val in players])


@bp.get(
    "/player/<name>",
    summary="return one specific player",
    tags=[player_tag],
    responses={200: RootModel[list[Player]]},
)
def get_one_player(path: PathName):
    db = get_db()
    player = db.execute(
        "SELECT * FROM jogador WHERE nome_jogador=?", [path.name]
    ).fetchone()
    return Player.models_to_json(Player.from_db(player))


@bp.get(
    "/coach",
    summary="return all coaches",
    tags=[coach_tag],
    responses={200: RootModel[list[Coach]]},
)
def get_all_coaches() -> list[Coach]:
    db = get_db()
    coaches = db.execute("SELECT * FROM tecnico ").fetchall()
    return Coach.models_to_json([Coach.from_db(val) for val in coaches])


@bp.get(
    "/coach/<name>",
    summary="return one specific coach",
    tags=[coach_tag],
    responses={200: RootModel[list[Coach]]},
)
def get_one_coach(path: PathName):
    db = get_db()
    coach = db.execute(
        "SELECT * FROM tecnico WHERE nome_tecnico=?", [path.name]
    ).fetchone()
    return Coach.models_to_json(Coach.from_db(coach))


@bp.get(
    "/match",
    summary="return all matches",
    tags=[match_tag],
    responses={200: RootModel[list[Match]]},
)
def get_all_matches() -> list[Match]:
    db = get_db()
    matches = db.execute("SELECT * FROM partida").fetchall()
    return Match.models_to_json([Match.from_db(val) for val in matches])


@bp.get(
    "/match/<int:id>",
    summary="return one specific match",
    tags=[match_tag],
    responses={200: RootModel[list[Match]]},
)
def get_one_match(path: PathID):
    db = get_db()
    match = db.execute("SELECT * FROM partida WHERE id_partida=?", [path.id]).fetchone()
    return Match.models_to_json(Match.from_db(match))


@bp.get(
    "/event",
    summary="return all events",
    tags=[event_tag],
    responses={200: RootModel[list[Event]]},
)
def get_all_events() -> list[Event]:
    db = get_db()
    events = db.execute("SELECT * FROM evento").fetchall()
    return Event.models_to_json([Event.from_db(val) for val in events])


@bp.get(
    "/event/<int:id>",
    summary="return all events",
    tags=[event_tag],
    responses={200: RootModel[list[Event]]},
)
def get_one_event(path: PathID):
    db = get_db()
    event = db.execute("SELECT * FROM evento WHERE id_evento=?", [path.id]).fetchone()
    return Event.models_to_json(Event.from_db(event))
