from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Question Routes
from app.server.api.v1.endpoints import router as ProcessDocument


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ProcessDocument, tags=["Processing Document"], prefix="/process_document")

@app.get('/', tags=["Root"])
async def start_root() -> dict:
    return {"Message": "AfternoonPrep brings together exam prep resources, interactive tests, and a collaborative community of peer-support, tailored to fit the African student’s needs."}