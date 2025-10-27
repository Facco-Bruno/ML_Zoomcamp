import pickle
from sklearn.pipeline import Pipeline

record = {
    "lead_source": "paid_ads",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0
}

with open("pipeline_v1.bin", "rb") as f:
    pipeline: Pipeline = pickle.load(f)

proba = float(pipeline.predict_proba([record])[0, 1])
print(f"{proba:.3f}")