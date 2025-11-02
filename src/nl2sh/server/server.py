import asyncio

from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import FastAPI, Request
from starlette import status
from nl2sh.models import (
    get_model_and_tokenizer,
    generate_stream,
)

app = FastAPI()

server_ready = None
model, tokenizer = None, None


@app.on_event("startup")
async def startup_event():
    global model, tokenizer, server_ready
    model, tokenizer = get_model_and_tokenizer()
    server_ready = True


@app.get("/api/ready")
async def is_ready():
    if not server_ready:
        return {"status": "success", "is_ready": False}

    return {"status": "success", "is_ready": True}


@app.post("/api/generate-stream")
async def generate_answer_stream(request: Request):
    """Stream the model response."""

    if not server_ready:
        return JSONResponse({"error": "Server is not ready yet"}, status_code=503)

    try:
        data = await request.json()
        if not data.get("prompt"):
            raise KeyError('the key "prompt" is not in the request.')

        streamer = generate_stream(model, tokenizer, data.get("prompt"))

        async def event_generator():
            for chunk in streamer:
                yield chunk
                await asyncio.sleep(0.01)

        return StreamingResponse(event_generator(), media_type="text/plain")
    except Exception as e:
        return {"status": "error", "err": str(e), "err_type": str(type(e))}
