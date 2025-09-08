from fastapi import FastAPI, Request
from dispatcher import handle_request # type: ignore
import uvicorn

app = FastAPI()

@app.post("/")
async def entry(request: Request) -> dict:
    """
    FastAPI entrypoint—handles all requests, returns errors for bad data.
    """
    try:
        payload = await request.json()
    except Exception:
        return {"error": "Could not parse JSON request."}
    
    response = handle_request(payload)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
