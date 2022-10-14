import orjson
from knappe import HTTPError
from tinydb.table import Document
from knappe.decorators import json, html, context
from knappe import HTTPError, Response
from kavalkade.controllers import router
from kavalkade.app.models import ModelInfo


@router.register("/api/characters")
@json
def list_characters(request) -> Response:
    model = request.app.models['character']
    table = request.app.database.table(model.table)
    return table.all()


@router.register("/api/characters/new", methods=('POST',))
@json
def new_character(request) -> Response:
    model = request.app.models['character']
    table = request.app.database.table(model.table)
    instance = model.model(**request.data.json)
    insert_id = table.insert(orjson.loads(instance.json()))
    return {'id': insert_id}


@router.register("/api/character/{id}/edit", methods=('POST',))
@json
def edit_character(request) -> Response:
    model = request.app.models['character']
    table = request.app.database.table(model.table)
    instance = model.model(**request.data.json)
    table.upsert(Document(request.data.json, docid=request.params['id']))
    return request.data.json


@router.register("/characters/new")
@router.register("/character/{id}/edit")
@html("jsonschema_form")
def character_form(request) -> dict:
    model = request.app.models['character']
    if character_id := request.params.get('id'):
        table = request.app.database.table(model.table)
        initial_data = table.get(doc_id=character_id)
        if initial_data is None:
            raise HTTPError(404)
        return {
            "initial_data": orjson.dumps(initial_data),
            "schema": model.schema,
            "action": f"/api/character/{character_id}/edit"
        }

    return {
        "initial_data": None,
        "schema": model.schema,
        "action": f"/api/characters/new"
    }


@router.register("/character/{id}")
def character_view(request) -> dict:
    model = request.app.models['character']
    table = request.app.database.table(model.table)
    doc = table.get(doc_id=request.params.get('id'))
    if doc is None:
        raise HTTPError(404)
    return Response.html(body=str(doc))


@router.register("/characters")
@html("characters")
def list_characters(request) -> Response:
    model = request.app.models['character']
    table = request.app.database.table(model.table)
    characters = []
    for doc in table.all():
        char = model.model(**doc)
        char._doc_id = doc.doc_id
        characters.append(char)
    return {'characters': characters}
