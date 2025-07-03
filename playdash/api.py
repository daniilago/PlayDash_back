from flask import Request, request
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
stats_tag = Tag(name="stats")


@bp.get(
    "/user",
    summary="return all users",
    tags=[user_tag],
    responses={200: RootModel[list[User]]},
)
def get_all_users() -> list[User]:
    db = get_db()
    users = db.execute("SELECT * FROM user ").fetchall()
    return User.models_to_json([User.from_db(val) for val in users])


@bp.get(
    "/user/<name>",
    summary="return one specific user",
    tags=[user_tag],
    responses={200: RootModel[list[User]]},
)
def get_one_user(path: PathName):
    db = get_db()
    user = db.execute("SELECT * FROM user WHERE name=?", [path.name]).fetchone()
    return User.models_to_json(User.from_db(user))


@bp.get(
    "/team",
    summary="return all teams",
    tags=[team_tag],
    responses={200: RootModel[list[Team]]},
)
def get_all_teams():
    db = get_db()
    teams = db.execute("SELECT * FROM team").fetchall()
    return Team.models_to_json([Team.from_db(val) for val in teams])


@bp.get(
    "/team/<name>",
    summary="return one specific team",
    tags=[team_tag],
    responses={200: RootModel[list[Team]]},
)
def get_one_team(path: PathName):
    db = get_db()
    team = db.execute("SELECT * FROM team WHERE name=?", [path.name]).fetchone()
    return Team.models_to_json(Team.from_db(team))


@bp.get(
    "/player",
    summary="return all players",
    tags=[player_tag],
    responses={200: RootModel[list[Player]]},
)
def get_all_players() -> list[Player]:
    db = get_db()
    team_name = request.args.get("team", None)
    if team_name is None:
        players = db.execute("SELECT * FROM player").fetchall()
    else:
        players = db.execute(
            "SELECT * FROM player WHERE team_name = ?", (team_name,)
        ).fetchall()
    return Player.models_to_json([Player.from_db(val) for val in players])


@bp.get(
    "/player/<name>",
    summary="return one specific player",
    tags=[player_tag],
    responses={200: RootModel[list[Player]]},
)
def get_one_player(path: PathName):
    db = get_db()
    player = db.execute("SELECT * FROM player WHERE name=?", [path.name]).fetchone()
    return Player.models_to_json(Player.from_db(player))


@bp.get(
    "/coach",
    summary="return all coaches",
    tags=[coach_tag],
    responses={200: RootModel[list[Coach]]},
)
def get_all_coaches() -> list[Coach]:
    db = get_db()
    coaches = db.execute("SELECT * FROM coach ").fetchall()
    return Coach.models_to_json([Coach.from_db(val) for val in coaches])


@bp.get(
    "/coach/<name>",
    summary="return one specific coach",
    tags=[coach_tag],
    responses={200: RootModel[list[Coach]]},
)
def get_one_coach(path: PathName):
    db = get_db()
    coach = db.execute("SELECT * FROM coach WHERE name=?", [path.name]).fetchone()
    return Coach.models_to_json(Coach.from_db(coach))


@bp.get(
    "/match",
    summary="return all matches",
    tags=[match_tag],
    responses={200: RootModel[list[Match]]},
)
def get_all_matches() -> list[Match]:
    db = get_db()
    filter = request.args.get("date", None)
    if filter is None:
        matches = db.execute("SELECT * FROM match").fetchall()
    elif filter == "past":
        matches = db.execute(
            "SELECT * FROM match where date_hour < datetime('now', '-2 hours')"
        ).fetchall()
    elif filter == "today":
        matches = db.execute(
            "SELECT * FROM match where date_hour >= datetime('now', '-2 hours') AND date_hour < date('now', '+1 day')"
        ).fetchall()
    elif filter == "week":
        matches = db.execute(
            "SELECT * FROM match where date_hour > date() AND date_hour <= date('now', 'weekday 6')"
        ).fetchall()
    elif filter == "future":
        matches = db.execute(
            "SELECT * FROM match where date_hour > date('now', 'weekday 6')"
        ).fetchall()
    return Match.models_to_json([Match.from_db(val) for val in matches])


@bp.get(
    "/match/<int:id>",
    summary="return one specific match",
    tags=[match_tag],
    responses={200: RootModel[list[Match]]},
)
def get_one_match(path: PathID):
    db = get_db()
    match = db.execute("SELECT * FROM match WHERE id=?", [path.id]).fetchone()
    return Match.models_to_json(Match.from_db(match))


@bp.get(
    "/event",
    summary="return all events",
    tags=[event_tag],
    responses={200: RootModel[list[Event]]},
)
def get_all_events() -> list[Event]:
    db = get_db()
    events = db.execute("SELECT * FROM event").fetchall()
    return Event.models_to_json([Event.from_db(val) for val in events])


@bp.get(
    "/event/<int:id>",
    summary="return all events",
    tags=[event_tag],
    responses={200: RootModel[list[Event]]},
)
def get_one_event(path: PathID):
    db = get_db()
    event = db.execute("SELECT * FROM event WHERE id=?", [path.id]).fetchone()
    return Event.models_to_json(Event.from_db(event))


@bp.get(
    "/stats/best_player",
    summary="return the best player (most goals, less penalties)",
    tags=[stats_tag],
    responses={200: RootModel[list[Player]]},
)
def get_best_player():
    db = get_db()
    player = db.execute("""SELECT * FROM player
                        ORDER BY goals DESC, red_cards ASC, yellow_cards ASC, fouls ASC
                        LIMIT 1""").fetchone()
    return Player.models_to_json(Player.from_db(player))


@bp.get(
    "/stats/worst_player",
    summary="return the worst player (least goals, most penalties)",
    tags=[stats_tag],
    responses={200: RootModel[list[Player]]},
)
def get_worst_player():
    db = get_db()
    player = db.execute("""SELECT * FROM player
                        ORDER BY goals ASC, red_cards DESC, yellow_cards DESC, fouls DESC
                        LIMIT 1""").fetchone()
    return Player.models_to_json(Player.from_db(player))


@bp.get(
    "/stats/player_fair_play",
    summary="return the player with the least penalties",
    tags=[stats_tag],
    responses={200: RootModel[list[Player]]},
)
def get_player_fair_play():
    db = get_db()
    player = db.execute("""SELECT * FROM player
                        ORDER BY red_cards ASC, yellow_cards ASC, fouls ASC
                        LIMIT 1""").fetchone()
    return Player.models_to_json(Player.from_db(player))


@bp.get(
    "/stats/player_foul_play",
    summary="return the player with the most penalties",
    tags=[stats_tag],
    responses={200: RootModel[list[Player]]},
)
def get_player_foul_play():
    db = get_db()
    player = db.execute("""SELECT * FROM player
                        ORDER BY red_cards DESC, yellow_cards DESC, fouls DESC
                        LIMIT 1""").fetchone()
    return Player.models_to_json(Player.from_db(player))


@bp.get(
    "/stats/team_fair_play",
    summary="return the team with the least penalties",
    tags=[stats_tag],
    responses={200: RootModel[list[Team]]},
)
def get_team_fair_play():
    db = get_db()
    team = db.execute("""SELECT * FROM team
                        ORDER BY red_cards ASC, yellow_cards ASC, fouls ASC
                        LIMIT 1""").fetchone()
    return Team.models_to_json(Team.from_db(team))


@bp.get(
    "/stats/team_foul_play",
    summary="return the team with the most penalties",
    tags=[stats_tag],
    responses={200: RootModel[list[Team]]},
)
def get_team_foul_play():
    db = get_db()
    team = db.execute("""SELECT * FROM team
                        ORDER BY red_cards DESC, yellow_cards DESC, fouls DESC
                        LIMIT 1""").fetchone()
    return Team.models_to_json(Team.from_db(team))
