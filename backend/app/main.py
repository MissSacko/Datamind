from fastapi import FastAPI

app = FastAPI(title="DataMind API")
    
@app.get("/")
def root():
    return {"message": "DataMind API is running"}