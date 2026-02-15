from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, generate

app = FastAPI(title="AI Answer Evaluator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(generate.router, prefix="/api", tags=["Generate"])

@app.get("/")
def read_root():
    return {"message": "AI Answer Evaluator API is running"}
