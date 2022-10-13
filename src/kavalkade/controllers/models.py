from knappe.decorators import json, html, context
from knappe import HTTPError, Response
from kavalkade.controllers import router
from kavalkade.app.models import ModelInfo


def get_model(request) -> ModelInfo:
    model = request.app.models.get(request.params["model"])
    if model is None:
        raise HTTPError(404)
    return model


def get_addable_model(request) -> ModelInfo:
    model = get_model(request)
    if not model.metadata.get("addable", False):
        raise HTTPError(403)
    return model


@router.register("/schemas/{model}")
@context(get_model)
def model_schema(request, model: ModelInfo) -> Response:
    return Response.from_json(200, body=model.schema)


@router.register("/models/{model}")
@html("jsonschema_form")
@context(get_addable_model)
def model_form(request, model: ModelInfo) -> dict:
    return {
        "schema": model.schema,
        "url": f"/schemas/{request.params['model']}",
        "action": f"/models/{request.params['model']}/save"
    }


@router.register("/models/{model}/save", methods=('POST',))
@json
@context(get_addable_model)
def model_save(request, model: ModelInfo) -> dict:
    instance = model.model(**request.data.json)
    return request.data.json
