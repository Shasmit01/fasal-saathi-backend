from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from prophet import Prophet
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(
    os.path.join(current_dir, "../../")
)

csv_path = os.path.join(
    project_root,
    "data",
    "processed",
    "commodity_prices.csv"
)

print("Using dataset:", csv_path)

df = pd.read_csv(csv_path)

@app.get("/")
def home():

    return {"message": "Fasal Saathi API working"}

@app.get("/forecast/{crop}")
def forecast(crop:str):

    crop_df = df[df["commodity"] == crop]

    crop_df = crop_df.rename(
        columns={
            "date":"ds",
            "price":"y"
        }
    )

    crop_df["ds"] = pd.to_datetime(crop_df["ds"])

    model = Prophet()

    model.fit(crop_df)

    future = model.make_future_dataframe(periods=7)

    forecast = model.predict(future)

    result = forecast[["ds","yhat"]].tail(1)

    return {

        "commodity": crop,

        "predicted_price":

        round(result.iloc[0]["yhat"],2)

    }