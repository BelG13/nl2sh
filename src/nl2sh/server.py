from fastapi.responses import StreamingResponse
import asyncio

from fastapi import FastAPI, Request
from nl2sh.model import (
    get_model_and_tokenizer,
    generate_stream,
)

model, tokenizer = get_model_and_tokenizer()
app = FastAPI()


@app.post("/api/generate-stream")
async def generate_answer_stream(request: Request):
    """Stream the model response."""

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
