from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_openapi3.blueprint import APIBlueprint

from playdash.db import get_db
from playdash.schema import Match
import json

from pydantic import RootModel, BaseModel

bp = APIBlueprint("api", __name__, url_prefix="/api")
match_tag = Tag(name="match")

@bp.get(
    "/match",
    summary="retorna todos os matches",
    tags=[match_tag],
    responses={200: RootModel[list[Match]]},
)
def get_all_matches() -> list[Match]:
    db = get_db()
    matches = db.execute("SELECT * FROM partida").fetchall()
    return Match.models_to_json([Match.from_db(val) for val in matches])

class PathID(BaseModel):
    id: int

@bp.get(
    "/match/<int:id>",
    summary="retorna todos os matches",
    tags=[match_tag],
    responses={200: RootModel[list[Match]]},
)
def get_one_match(path: PathID):
    db = get_db()
    match = db.execute("SELECT * FROM partida WHERE id_partida=?", [path.id]).fetchone()
    return Match.models_to_json(Match.from_db(match))