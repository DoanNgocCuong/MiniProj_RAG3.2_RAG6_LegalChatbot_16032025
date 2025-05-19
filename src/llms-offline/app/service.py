from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .inference import generate

class Request(BaseModel):
    prompt: str
    max_tokens: int = 128
    temperature: float = 0.7
    top_p: float = 0.9
    do_sample: bool = True

class Response(BaseModel):
    text: str

app = FastAPI(title="Llama-3.2-3B-Instruct-Frog API")

@app.post("/v1/generate", response_model=Response)
async def v1_generate(req: Request):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="`prompt` is required.")
    try:
        text = generate(
            prompt=req.prompt,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
            do_sample=req.do_sample
        )
        return Response(text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
