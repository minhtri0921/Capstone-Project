from dotenv import load_dotenv
load_dotenv(override=True)
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from graph import app as workflow
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage, AIMessage
from logger import logger

app = FastAPI(docs_url="/")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    messages: list = Field(..., description="List of messages")
    language: Optional[str] = Field("vi", description="Language of the messages")

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"type": "human", "content": "Chào bạn"},
                    {"type": "ai", "content": "Bạn muốn tìm job gì?"},
                    {
                        "type": "human",
                        "content": "Tôi muốn tìm job dạy học cho trung cấp",
                    },
                ],
                "language": "vi",
            }
        }


def convert_message(messages):
    list_message = []
    for message in messages:
        if message["type"] == "human":
            list_message.append(HumanMessage(content=message["content"]))
        else:
            list_message.append(AIMessage(content=message["content"]))
    return list_message


@app.post("/chat")
async def Chat(item: Item):
    messages = convert_message(item.messages)
    history = messages[:-1] if len(messages) > 1 else []
    try:
        response = workflow.invoke(
            {
                "user_query": messages[-1],
                "messages_history": history,
                "language": item.language,
            }
        )["llm_response"]
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))  
    uvicorn.run("app:app", host="0.0.0.0", port=port)
