from asyncio import sleep
import random

from pydantic import BaseModel, field_validator, ValidationError
from litestar import Litestar, post
from litestar.config.cors import CORSConfig
from litestar.response import Response


class SubmitRequest(BaseModel):
    date: str
    first_name: str
    last_name: str

    @field_validator("first_name")
    def check_first_name(cls, value):
        if " " in value:
            raise ValueError("No whitespace in first name is allowed")
        return value

    @field_validator("last_name")
    def check_last_name(cls, value):
        if " " in value:
            raise ValueError("No whitespace in last name is allowed")
        return value

@post("/api/submit")
async def submit(data: dict[str, str]) -> Response:
    await sleep(random.uniform(0, 2.5))
    try:
        form_data = SubmitRequest(**data)
    except ValidationError as e:
        error_msg = {}
        for error in e.errors():
            field = error["loc"][0]
            msg = error["ctx"]["error"]
            error_msg[field] = [str(msg)]
        return Response(content={"success": False, "error": error_msg}, status_code=400)

    data = {
        "date": form_data.date,
        "name": f"{form_data.first_name} {form_data.last_name}",
    }

    return Response(content={"success": True, "data": [data] * random.randint(2, 5)})


cors_config = CORSConfig(allow_origins=["*"], allow_methods=["POST", "OPTIONS"])

app = Litestar(
    route_handlers=[submit],
    cors_config=cors_config,
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
