from kavalkade.controllers import router
from knappe.decorators import json, html, context
from knappe import HTTPError, Response


def get_model(request):
    model = request.app.models.get(request.params["model"])
    if model is None:
        raise HTTPError(404)
    return model


@router.register("/schemas/{model}")
@json
@context(get_model)
def model_schema(request, model):
    return Response.from_json(200, body=model.schema)


@router.register("/models/{model}")
@html("jsonschema_form")
@context(get_model)
def model_form(request, model):
    return {
        "schema": model.schema,
        "url": f"/schemas/{request.params['model']}",
        "action": f"/models/{request.params['model']}/save"
    }


@router.register("/models/{model}/save", methods=('POST',))
@json
@context(get_model)
def model_save(request, model):
    instance = model.model(**request.data.json)
    print(repr(instance))
