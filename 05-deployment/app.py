import pickle
from typing import TypedDict
from fastapi import FastAPI

class Lead(TypedDict):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float

app = FastAPI()

with open("pipeline_v1.bin", "rb") as f:
    pipeline = pickle.load(f)

@app.get("/")
def home():
    return {"ok": True}

@app.post("/predict")
def predict(lead: Lead):
    proba = float(pipeline.predict_proba([dict(lead)])[0, 1])
    return {"conversion_probability": proba}