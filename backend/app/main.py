from fastapi import FastAPI

from app.api.v1.users import router as users_router


app = FastAPI(title="DataMind API")


@app.get("/")
def root():
    return {"message": "DataMind API is running"}


app.include_router(
    users_router,
    prefix="/api/v1",
)