from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse
from transformers import pipeline
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat")
async def chat(llm1: str, llm2: str, topic: str, messages: int):
    async def event_generator():
        conversation = [f"Discuss the topic: {topic}"]
        for _ in range(messages):
            for llm in [llm1, llm2]:
                response = await get_llm_response(llm, conversation)
                conversation.append(response)
                yield {
                    "event": "new_message",
                    "data": {"llm": llm, "message": response}
                }
                await asyncio.sleep(0.1)

    return EventSourceResponse(event_generator())

# chucking stuff at it for now, will edit when backend/models etc are finalised

async def get_llm_response(llm, conversation):
    generator = pipeline('text-generation', model=llm)
    response = generator(conversation[-1], max_length=100)
    return response[0]['generated_text']

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)