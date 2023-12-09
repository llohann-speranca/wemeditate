from typing import Optional

from fastapi import FastAPI
from wemeditate.syretriever.agent import Agent
from wemeditate.constants import K
app = FastAPI()
agent = Agent()

@app.get("/retriever/")
async def read_item(query: str, k: Optional[int] = K):
    return agent(query, k)
