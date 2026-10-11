from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import joblib
import pandas as pd
import os

from datetime import datetime

from backend.weather import get_weather
from backend.fertilizer import recommend_fertilizer
from backend.irrigation import recommend_irrigation
from backend.database_api import router as database_router
from backend.reports import router as reports_router
from backend.leaf_disease import router as leaf_disease_router

from backend.what_if import (
    WhatIfRequest,
    WhatIfResponse,
    calculate_what_if
)

from database.database import get_db
from database.models import PredictionHistory


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Crop Intelligence API",
    description=(
        "AI-powered agricultural decision support system with "
        "crop yield prediction, crop recommendation, weather, "
        "fertilizer, irrigation, farmer management, prediction "
        "history, What-If analysis and advanced smart farming modules."
    ),
    version="6.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(database_router)
app.include_router(reports_router)
app.include_router(leaf_disease_router)

# ============================================================
# MODEL PATHS
# ============================================================

YIELD_MODEL_PATH = (
    r"C:\AI_Crop_Optimization\models\yield_random_forest.joblib"
)

CROP_MODEL_PATH = (
    r"C:\AI_Crop_Optimization\models\crop_recommendation_model.joblib"
)

EXPLAINABILITY_PATH = (
    r"C:\AI_Crop_Optimization\data\processed"
    r"\explainable_ai_importance.csv"
)

HISTORICAL_DATA_PATH = (
    r"C:\AI_Crop_Optimization\data\processed"
    r"\crop_yield_india_clean.csv"
)

RAW_DATA_PATH = (
    r"C:\AI_Crop_Optimization\data\raw"
    r"\crop_yield_india.csv"
)


# ============================================================
# LOAD MODELS
# ============================================================

yield_model = joblib.load(YIELD_MODEL_PATH)
crop_model = joblib.load(CROP_MODEL_PATH)


# ============================================================
# REQUEST MODELS
# ============================================================

class CropInput(BaseModel):
    Crop: str
    Crop_Year: int
    Season: str
    State: str
    Area: float
    Annual_Rainfall: float
    Fertilizer: float
    Pesticide: float
    farmer_id: int | None = None
    farm_id: int | None = None




class PredictionHistoryUpdate(BaseModel):
    crop: str | None = None
    season: str | None = None
    state: str | None = None
    predicted_yield: float | None = None


class CropRecommendationInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


class WeatherInput(BaseModel):
    latitude: float
    longitude: float


class FertilizerInput(BaseModel):
    crop: str
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float


class IrrigationInput(BaseModel):
    crop: str
    area: float
    soil_moisture: float
    temperature: float
    rainfall: float
    growth_stage: str
    soil_type: str
    irrigation_method: str


# ============================================================
# HOME
# ============================================================

@app.get("/", response_model=dict)
def home():

    return {
        "message": "AI Crop Intelligence API is running!",
        "status": "success",
        "version": "6.0.0",

        "services": [

            "crop_yield_prediction",

            "crop_recommendation",

            "weather_forecast",

            "smart_fertilizer_recommendation",

            "smart_irrigation_recommendation",

            "what_if_simulation",

            "farmer_management",

            "farm_management",

            "prediction_history",

            "explainable_ai",

            "report_downloads",

            "risk_analysis",

            "ndvi_analysis",

            "iot_sensor_integration",

            "pest_disease_warning",

            "cnn_disease_detection",

            "crop_rotation",

            "best_sowing_date",

            "market_price",

            "profitability",

            "insurance_risk",

            "historical_yield_trend",

            "data_cleaning_status",

            "model_monitoring",

            "multi_language",

            "voice_input",

            "voice_output",

            "offline_mode",

            "notifications",

            "gis_field_boundary"
        ]
    }


# ============================================================
# CROP YIELD PREDICTION
# ============================================================

@app.post(
    "/predict",
    response_model=dict
)
def predict_yield(
    data: CropInput,
    db: Session = Depends(get_db)
):

    input_data = pd.DataFrame([
        {
            "Crop": data.Crop,
            "Crop_Year": data.Crop_Year,
            "Season": data.Season,
            "State": data.State,
            "Area": data.Area,
            "Annual_Rainfall": data.Annual_Rainfall,
            "Fertilizer": data.Fertilizer,
            "Pesticide": data.Pesticide
        }
    ])

    prediction = float(
        yield_model.predict(input_data)[0]
    )

    history_saved = False
    prediction_id = None

    if (
        data.farmer_id is not None
        and data.farm_id is not None
    ):

        prediction_history = PredictionHistory(

            farmer_id=data.farmer_id,

            farm_id=data.farm_id,

            crop=data.Crop,

            crop_year=data.Crop_Year,

            season=data.Season,

            state=data.State,

            area=data.Area,

            rainfall=data.Annual_Rainfall,

            fertilizer=data.Fertilizer,

            pesticide=data.Pesticide,

            predicted_yield=prediction
        )

        db.add(prediction_history)

        db.commit()

        db.refresh(prediction_history)

        history_saved = True

        prediction_id = prediction_history.id

    return {

        "crop": data.Crop,

        "state": data.State,

        "predicted_yield": round(
            prediction,
            4
        ),

        "history_saved": history_saved,

        "prediction_id": prediction_id
    }


# ============================================================
# WHAT-IF SCENARIO SIMULATOR
# ============================================================

@app.post(
    "/what-if",
    response_model=WhatIfResponse
)
def what_if_simulation(
    data: WhatIfRequest
):

    return calculate_what_if(data)


# ============================================================
# EXPLAINABLE AI
# ============================================================

@app.get(
    "/explainable-ai",
    response_model=dict
)
def explainable_ai():

    if not os.path.exists(
        EXPLAINABILITY_PATH
    ):

        return {
            "status": "error",
            "message": "Explainable AI results not found"
        }

    df = pd.read_csv(
        EXPLAINABILITY_PATH
    )

    top_features = df.head(10)

    return {

        "status": "success",

        "features": top_features.to_dict(
            orient="records"
        )
    }


# ============================================================
# CROP RECOMMENDATION
# ============================================================

@app.post(
    "/recommend-crop",
    response_model=dict
)
def recommend_crop(
    data: CropRecommendationInput
):

    input_data = pd.DataFrame([
        {
            "N": data.N,
            "P": data.P,
            "K": data.K,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "ph": data.ph,
            "rainfall": data.rainfall
        }
    ])

    recommended_crop = crop_model.predict(
        input_data
    )[0]

    return {

        "recommended_crop": str(
            recommended_crop
        )
    }


# ============================================================
# WEATHER
# ============================================================

@app.post(
    "/weather",
    response_model=dict
)
def weather_forecast(
    data: WeatherInput
):

    weather = get_weather(
        data.latitude,
        data.longitude
    )

    return {

        "latitude": data.latitude,

        "longitude": data.longitude,

        "current": weather["current"],

        "daily": weather["daily"]
    }


# ============================================================
# FERTILIZER RECOMMENDATION
# ============================================================

@app.post(
    "/fertilizer",
    response_model=dict
)
def fertilizer_recommendation(
    data: FertilizerInput
):

    return recommend_fertilizer(

        crop=data.crop,

        nitrogen=data.nitrogen,

        phosphorus=data.phosphorus,

        potassium=data.potassium,

        ph=data.ph
    )


# ============================================================
# IRRIGATION RECOMMENDATION
# ============================================================

@app.post(
    "/irrigation",
    response_model=dict
)
def irrigation_recommendation(
    data: IrrigationInput
):

    return recommend_irrigation(

        crop=data.crop,

        area=data.area,

        soil_moisture=data.soil_moisture,

        temperature=data.temperature,

        rainfall=data.rainfall,

        growth_stage=data.growth_stage,

        soil_type=data.soil_type,

        irrigation_method=data.irrigation_method
    )


# ============================================================
# EXTREME WEATHER & DROUGHT RISK
# ============================================================

class RiskInput(BaseModel):

    crop: str

    rainfall_mm: float

    temperature_c: float

    humidity_percent: float

    soil_moisture_percent: float


@app.post(
    "/risk-analysis",
    response_model=dict
)
def risk_analysis(
    data: RiskInput
):

    risk_score = 0

    if data.rainfall_mm < 500:

        risk_score += 30

    elif data.rainfall_mm < 800:

        risk_score += 15


    if data.temperature_c > 38:

        risk_score += 25

    elif data.temperature_c > 35:

        risk_score += 15


    if data.humidity_percent < 35:

        risk_score += 20

    elif data.humidity_percent < 50:

        risk_score += 10


    if data.soil_moisture_percent < 20:

        risk_score += 25

    elif data.soil_moisture_percent < 35:

        risk_score += 10


    risk_score = min(
        risk_score,
        100
    )


    if risk_score >= 70:

        risk_level = "High"

        recommendation = (
            "High agricultural risk. Increase irrigation "
            "monitoring and prepare for extreme weather."
        )

    elif risk_score >= 40:

        risk_level = "Medium"

        recommendation = (
            "Moderate risk. Monitor rainfall, temperature "
            "and soil moisture regularly."
        )

    else:

        risk_level = "Low"

        recommendation = (
            "Low current risk. Continue normal farm monitoring."
        )


    return {

        "status": "success",

        "crop": data.crop,

        "risk_score": risk_score,

        "risk_level": risk_level,

        "recommendation": recommendation
    }


# ============================================================
# SATELLITE / NDVI
# ============================================================

class NDVIInput(BaseModel):

    latitude: float

    longitude: float

    field_id: str

    ndvi: float


@app.post(
    "/ndvi",
    response_model=dict
)
def ndvi_analysis(
    data: NDVIInput
):

    ndvi = data.ndvi


    if ndvi >= 0.7:

        health = "Excellent"

        recommendation = (
            "Crop vegetation appears very healthy."
        )

    elif ndvi >= 0.5:

        health = "Good"

        recommendation = (
            "Crop health is good. Continue normal monitoring."
        )

    elif ndvi >= 0.3:

        health = "Moderate"

        recommendation = (
            "Monitor crop stress, irrigation and nutrients."
        )

    elif ndvi >= 0.1:

        health = "Poor"

        recommendation = (
            "Possible crop stress. Inspect the field."
        )

    else:

        health = "Very Poor"

        recommendation = (
            "Very low vegetation signal. "
            "Field inspection recommended."
        )


    return {

        "status": "success",

        "field_id": data.field_id,

        "latitude": data.latitude,

        "longitude": data.longitude,

        "ndvi": data.ndvi,

        "crop_health": health,

        "recommendation": recommendation,

        "provider_status": (
            "NDVI analysis ready; satellite provider "
            "can be connected."
        )
    }


# ============================================================
# REAL-TIME IOT SENSOR INTEGRATION
# ============================================================

class IoTSensorInput(BaseModel):

    device_id: str

    soil_moisture: float

    temperature: float

    soil_ph: float

    timestamp: str | None = None


@app.post(
    "/iot/sensors",
    response_model=dict
)
def iot_sensor_data(
    data: IoTSensorInput
):

    if data.soil_moisture < 25:

        moisture_status = "Low"

        irrigation_status = (
            "Irrigation may be required"
        )

    elif data.soil_moisture < 50:

        moisture_status = "Moderate"

        irrigation_status = (
            "Monitor soil moisture"
        )

    else:

        moisture_status = "Good"

        irrigation_status = (
            "No immediate irrigation required"
        )


    return {

        "status": "success",

        "device_id": data.device_id,

        "soil_moisture": data.soil_moisture,

        "temperature": data.temperature,

        "soil_ph": data.soil_ph,

        "moisture_status": moisture_status,

        "irrigation_status": irrigation_status,

        "received_at": (
            data.timestamp
            or datetime.now().isoformat()
        )
    }


# ============================================================
# PEST & DISEASE OUTBREAK WARNING
# ============================================================

class PestDiseaseInput(BaseModel):

    crop: str

    temperature_c: float

    humidity_percent: float

    rainfall_mm: float

    soil_moisture: float = 0


@app.post(
    "/pest-disease-warning",
    response_model=dict
)
def pest_disease_warning(
    data: PestDiseaseInput
):

    risk_score = 0


    if data.humidity_percent >= 80:

        risk_score += 35

    elif data.humidity_percent >= 65:

        risk_score += 20


    if data.temperature_c >= 30:

        risk_score += 25

    elif data.temperature_c >= 25:

        risk_score += 15


    if data.rainfall_mm >= 150:

        risk_score += 30

    elif data.rainfall_mm >= 80:

        risk_score += 15


    risk_score = min(
        risk_score,
        100
    )


    if risk_score >= 70:

        level = "High"

        message = (
            "High pest/disease outbreak risk. "
            "Field inspection is strongly recommended."
        )

    elif risk_score >= 40:

        level = "Medium"

        message = (
            "Moderate outbreak risk. Monitor crop leaves "
            "and field conditions."
        )

    else:

        level = "Low"

        message = (
            "Low current outbreak risk."
        )


    return {

        "status": "success",

        "crop": data.crop,

        "risk_score": risk_score,

        "risk_level": level,

        "message": message
    }


# ============================================================
# CNN LEAF IMAGE PEST / DISEASE DETECTION
# ============================================================

@app.post(
    "/disease-detection",
    response_model=dict
)
async def disease_detection(
    file: UploadFile = File(...)
):

    filename = file.filename or ""


    allowed_extensions = (

        ".jpg",

        ".jpeg",

        ".png",

        ".webp"
    )


    if not filename.lower().endswith(
        allowed_extensions
    ):

        return {

            "status": "error",

            "filename": filename,

            "message": (
                "Please upload JPG, JPEG, PNG or WEBP image."
            ),

            "prediction": None
        }


    return {

        "status": "provider_ready",

        "filename": filename,

        "message": (
            "Leaf image received successfully. "
            "CNN model endpoint is ready for trained "
            "model integration."
        ),

        "prediction": (
            "CNN model not connected yet"
        )
    }


# ============================================================
# CROP ROTATION ADVISOR
# ============================================================

class CropRotationInput(BaseModel):

    current_crop: str

    soil_type: str

    season: str


@app.post(
    "/crop-rotation",
    response_model=dict
)
def crop_rotation(
    data: CropRotationInput
):

    crop = data.current_crop.lower()


    rotation_map = {

        "rice": [

            "Green gram",

            "Black gram",

            "Groundnut"
        ],

        "wheat": [

            "Pulses",

            "Chickpea",

            "Mustard"
        ],

        "maize": [

            "Soybean",

            "Groundnut",

            "Pulses"
        ],

        "cotton": [

            "Groundnut",

            "Pulses",

            "Sorghum"
        ],

        "sugarcane": [

            "Pulses",

            "Green manure",

            "Groundnut"
        ]
    }


    recommendations = rotation_map.get(

        crop,

        [

            "Pulses",

            "Legumes",

            "Green manure"
        ]
    )


    return {

        "status": "success",

        "current_crop": data.current_crop,

        "soil_type": data.soil_type,

        "season": data.season,

        "recommended_rotation": recommendations,

        "reason": (
            "Crop rotation can improve soil health "
            "and reduce repeated crop-related risks."
        )
    }


# ============================================================
# BEST SOWING DATE
# ============================================================

class SowingDateInput(BaseModel):

    crop: str

    state: str

    season: str


@app.post(
    "/best-sowing-date",
    response_model=dict
)
def best_sowing_date(
    data: SowingDateInput
):

    sowing_calendar = {

        "kharif": "June - July",

        "rabi": "October - December",

        "summer": "January - March",

        "whole year": (
            "Based on local weather and "
            "irrigation availability"
        )
    }


    recommended_period = sowing_calendar.get(

        data.season.lower(),

        "Based on local climate and soil conditions"
    )


    return {

        "status": "success",

        "crop": data.crop,

        "state": data.state,

        "season": data.season,

        "recommended_sowing_period": (
            recommended_period
        ),

        "note": (
            "For production use, connect live weather "
            "and regional agricultural calendar data."
        )
    }


# ============================================================
# MARKET PRICE / MANDI / MSP
# ============================================================

class MarketPriceInput(BaseModel):

    crop: str

    state: str

    market: str


@app.post(
    "/market-price",
    response_model=dict
)
def market_price(
    data: MarketPriceInput
):

    return {

        "status": "provider_ready",

        "crop": data.crop,

        "state": data.state,

        "market": data.market,

        "market_price": None,

        "unit": "per ton",

        "message": (
            "Market/Mandi provider is ready "
            "for API integration."
        )
    }


# ============================================================
# PROFITABILITY
# ============================================================

class ProfitabilityInput(BaseModel):

    yield_ton_per_hectare: float

    area_hectare: float

    market_price_per_ton: float

    input_cost: float


@app.post(
    "/profitability",
    response_model=dict
)
def profitability(
    data: ProfitabilityInput
):

    total_production = (

        data.yield_ton_per_hectare

        * data.area_hectare
    )


    revenue = (

        total_production

        * data.market_price_per_ton
    )


    profit = revenue - data.input_cost


    if revenue > 0:

        profit_margin = (
            profit / revenue
        ) * 100

    else:

        profit_margin = 0


    return {

        "status": "success",

        "total_production_ton": round(
            total_production,
            4
        ),

        "revenue": round(
            revenue,
            2
        ),

        "input_cost": round(
            data.input_cost,
            2
        ),

        "estimated_profit": round(
            profit,
            2
        ),

        "profit_margin_percent": round(
            profit_margin,
            2
        )
    }


# ============================================================
# INSURANCE RISK
# ============================================================

class InsuranceRiskInput(BaseModel):

    crop: str

    area_hectare: float

    rainfall_mm: float

    temperature_c: float


@app.post(
    "/insurance-risk",
    response_model=dict
)
def insurance_risk(
    data: InsuranceRiskInput
):

    risk_score = 0


    if data.rainfall_mm < 500:

        risk_score += 40

    elif data.rainfall_mm > 2500:

        risk_score += 30


    if data.temperature_c > 40:

        risk_score += 40

    elif data.temperature_c > 35:

        risk_score += 20


    risk_score = min(
        risk_score,
        100
    )


    if risk_score >= 70:

        level = "High"

    elif risk_score >= 40:

        level = "Medium"

    else:

        level = "Low"


    return {

        "status": "success",

        "crop": data.crop,

        "area_hectare": data.area_hectare,

        "risk_score": risk_score,

        "risk_level": level,

        "message": (
            "Insurance risk screening completed."
        )
    }


# ============================================================
# HISTORICAL YIELD TREND
# ============================================================

class HistoricalTrendInput(BaseModel):

    crop: str

    state: str


@app.post(
    "/historical-trend",
    response_model=dict
)
def historical_trend(
    data: HistoricalTrendInput
):

    if not os.path.exists(
        HISTORICAL_DATA_PATH
    ):

        return {

            "status": "error",

            "crop": data.crop,

            "state": data.state,

            "records": [],

            "record_count": 0,

            "message": (
                "Historical dataset not found."
            )
        }


    df = pd.read_csv(
        HISTORICAL_DATA_PATH
    )


    filtered = df[

        (

            df["Crop"]

            .astype(str)

            .str.lower()

            == data.crop.lower()
        )

        &

        (

            df["State"]

            .astype(str)

            .str.lower()

            == data.state.lower()
        )

    ].copy()


    if filtered.empty:

        return {

            "status": "success",

            "crop": data.crop,

            "state": data.state,

            "records": [],

            "record_count": 0,

            "message": (
                "No historical records found for "
                "the selected crop and state."
            )
        }


    trend = (

        filtered

        .groupby("Crop_Year")["Yield"]

        .mean()

        .reset_index()

        .sort_values("Crop_Year")
    )


    records = [

        {

            "year": int(
                row["Crop_Year"]
            ),

            "average_yield": round(
                float(row["Yield"]),
                4
            )
        }

        for _, row in trend.iterrows()
    ]


    return {

        "status": "success",

        "crop": data.crop,

        "state": data.state,

        "records": records,

        "record_count": len(records)
    }


# ============================================================
# DATA CLEANING STATUS
# ============================================================

@app.get(
    "/data-cleaning-status",
    response_model=dict
)
def data_cleaning_status():

    return {

        "status": "success",

        "raw_dataset_exists": os.path.exists(
            RAW_DATA_PATH
        ),

        "clean_dataset_exists": os.path.exists(
            HISTORICAL_DATA_PATH
        ),

        "pipeline_status": (

            "Completed"

            if os.path.exists(
                HISTORICAL_DATA_PATH
            )

            else "Not completed"
        ),

        "raw_dataset": RAW_DATA_PATH,

        "clean_dataset": HISTORICAL_DATA_PATH
    }


# ============================================================
# MODEL MONITORING
# ============================================================

@app.get(
    "/model-monitoring",
    response_model=dict
)
def model_monitoring():

    model_exists = os.path.exists(
        YIELD_MODEL_PATH
    )


    return {

        "status": "success",

        "model": (
            "Random Forest Yield Prediction"
        ),

        "model_file_exists": model_exists,

        "model_path": YIELD_MODEL_PATH,

        "monitoring_status": (

            "Model available"

            if model_exists

            else "Model file not found"
        ),

        "retraining_status": (
            "Manual retraining pipeline ready"
        )
    }


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

@app.get(
    "/languages",
    response_model=dict
)
def supported_languages():

    return {

        "status": "success",

        "languages": [

            {
                "code": "en",
                "name": "English"
            },

            {
                "code": "ta",
                "name": "Tamil"
            },

            {
                "code": "hi",
                "name": "Hindi"
            },

            {
                "code": "te",
                "name": "Telugu"
            },

            {
                "code": "kn",
                "name": "Kannada"
            },

            {
                "code": "ml",
                "name": "Malayalam"
            },

            {
                "code": "mr",
                "name": "Marathi"
            },

            {
                "code": "bn",
                "name": "Bengali"
            }
        ]
    }


# ============================================================
# VOICE OUTPUT
# ============================================================

class VoiceOutputInput(BaseModel):

    text: str

    language: str = "en"


@app.post(
    "/voice/output",
    response_model=dict
)
def voice_output(
    data: VoiceOutputInput
):

    return {

        "status": "success",

        "language": data.language,

        "text": data.text,

        "message": (
            "Voice output request accepted. "
            "Browser speech synthesis can play the response."
        )
    }


# ============================================================
# VOICE INPUT
# ============================================================

class VoiceInputRequest(BaseModel):

    language: str = "en"


@app.post(
    "/voice/input",
    response_model=dict
)
def voice_input(
    data: VoiceInputRequest
):

    return {

        "status": "success",

        "language": data.language,

        "message": (
            "Voice input endpoint ready. "
            "Browser speech recognition can provide the transcript."
        )
    }


# ============================================================
# OFFLINE MODE
# ============================================================

@app.get(
    "/offline-status",
    response_model=dict
)
def offline_status():

    return {

        "status": "success",

        "offline_mode": True,

        "local_model_available": os.path.exists(
            YIELD_MODEL_PATH
        ),

        "local_dataset_available": os.path.exists(
            HISTORICAL_DATA_PATH
        ),

        "message": (
            "Core prediction and local data features "
            "can operate without external provider APIs."
        )
    }


# ============================================================
# SMS / WHATSAPP NOTIFICATION
# ============================================================

class NotificationInput(BaseModel):

    recipient: str

    message: str

    channel: str


@app.post(
    "/notifications/send",
    response_model=dict
)
def send_notification(
    data: NotificationInput
):

    channel = data.channel.lower()


    if channel not in [

        "sms",

        "whatsapp"
    ]:

        return {

            "status": "error",

            "recipient": data.recipient,

            "channel": channel,

            "message": (
                "Channel must be SMS or WhatsApp."
            ),

            "delivery_status": None
        }


    return {

        "status": "provider_ready",

        "recipient": data.recipient,

        "channel": channel,

        "message": data.message,

        "delivery_status": (
            "Provider credentials not connected"
        )
    }


# ============================================================
# GIS FARM BOUNDARY
# ============================================================

class GISFarmInput(BaseModel):

    boundary_points: str


@app.post(
    "/gis/farm",
    response_model=dict
)
def process_gis_farm(
    data: GISFarmInput
):

    try:

        points = []


        for line in (

            data.boundary_points

            .strip()

            .splitlines()
        ):

            lat, lon = line.split(",")


            points.append(

                {

                    "latitude": float(
                        lat.strip()
                    ),

                    "longitude": float(
                        lon.strip()
                    )
                }
            )


        if len(points) < 3:

            return {

                "status": "error",

                "point_count": len(points),

                "boundary": points,

                "message": (
                    "At least 3 boundary points "
                    "are required."
                )
            }


        return {

            "status": "success",

            "point_count": len(points),

            "boundary": points,

            "message": (
                "Farm boundary processed successfully."
            )
        }


    except Exception:

        return {

            "status": "error",

            "point_count": 0,

            "boundary": [],

            "message": (
                "Invalid boundary format. "
                "Use latitude,longitude per line."
            )
        }


# ============================================================
# END OF AI CROP INTELLIGENCE API
# ============================================================

# ============================================================
# PREDICTION HISTORY UPDATE AND DELETE
# ============================================================

@app.put("/prediction-history/{prediction_id}", response_model=dict)
def update_prediction_history(
    prediction_id: int,
    data: PredictionHistoryUpdate,
    db: Session = Depends(get_db),
):
    record = (
        db.query(PredictionHistory)
        .filter(PredictionHistory.id == prediction_id)
        .first()
    )
    if record is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Prediction history record not found")

    updates = data.model_dump(exclude_unset=True)
    if "crop" in updates:
        crop = updates["crop"]
        if crop is None or not crop.strip():
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Crop cannot be empty")
        updates["crop"] = crop.strip()
    if "season" in updates and updates["season"] is not None:
        updates["season"] = updates["season"].strip() or None
    if "state" in updates and updates["state"] is not None:
        updates["state"] = updates["state"].strip() or None
    if "predicted_yield" in updates:
        value = updates["predicted_yield"]
        if value is None or value < 0:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail="Predicted yield must be a non-negative number",
            )

    for field, value in updates.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return {
        "message": "Prediction history updated successfully",
        "id": record.id,
        "farmer_id": record.farmer_id,
        "farm_id": record.farm_id,
        "crop": record.crop,
        "crop_year": record.crop_year,
        "season": record.season,
        "state": record.state,
        "area": record.area,
        "rainfall": record.rainfall,
        "fertilizer": record.fertilizer,
        "pesticide": record.pesticide,
        "predicted_yield": record.predicted_yield,
        "created_at": record.created_at.isoformat() if record.created_at else None,
    }


@app.delete("/prediction-history/{prediction_id}", response_model=dict)
def delete_prediction_history(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(PredictionHistory)
        .filter(PredictionHistory.id == prediction_id)
        .first()
    )
    if record is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Prediction history record not found")

    db.delete(record)
    db.commit()
    return {
        "message": "Prediction history deleted successfully",
        "prediction_id": prediction_id,
    }

