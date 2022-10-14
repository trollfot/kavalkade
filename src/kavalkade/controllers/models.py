from knappe import HTTPError, Response
from kavalkade.controllers import router
from kavalkade.app.models import ModelInfo


@router.register("/schemas/{model}")
def model_schema(request, model: ModelInfo) -> Response:
    model = request.app.models.get(request.params["model"])
    if model is None:
        raise HTTPError(404)
    return Response.from_json(200, body=model.schema)
