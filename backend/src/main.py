from asyncio import sleep
import random

from pydantic import BaseModel, field_validator, ValidationError
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn


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


async def submit(request):
    data = await request.json()
    await sleep(random.uniform(0, 2.5))
    try:
        form_data = SubmitRequest(**data)
    except ValidationError as e:
        error_msg = {}
        for error in e.errors():
            field = error["loc"][0]
            msg = error["ctx"]["error"]
            error_msg[field] = [str(msg)]
        return JSONResponse(
            {"success": False, "error": error_msg},
            status_code=400,
        )

    data = {
        "date": form_data.date,
        "name": f"{form_data.first_name} {form_data.last_name}",
    }

    return JSONResponse({"success": True, "data": [data] * random.randint(2, 5)})


routes = [
    Route("/api/submit", submit, methods=["POST"]),
]

middleware = [Middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["POST", "OPTIONS"]
)]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
