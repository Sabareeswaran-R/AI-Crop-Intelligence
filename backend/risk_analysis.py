from pydantic import BaseModel


class RiskAnalysisRequest(BaseModel):
    rainfall_mm: float
    temperature_c: float
    soil_moisture_percent: float
    humidity_percent: float
    crop_stage: str = "Vegetative"


class RiskAnalysisResponse(BaseModel):
    drought_risk: str
    extreme_weather_risk: str
    overall_risk: str
    risk_score: float
    recommendation: str


def analyze_risk(data: RiskAnalysisRequest) -> RiskAnalysisResponse:

    score = 0.0

    # Drought risk
    if data.rainfall_mm < 500:
        score += 30
    elif data.rainfall_mm < 800:
        score += 15

    if data.soil_moisture_percent < 20:
        score += 30
    elif data.soil_moisture_percent < 35:
        score += 15

    # Extreme temperature risk
    if data.temperature_c >= 40:
        score += 25
    elif data.temperature_c >= 35:
        score += 15

    # Humidity contribution
    if data.humidity_percent < 30:
        score += 10
    elif data.humidity_percent > 90:
        score += 10

    score = min(score, 100)

    # Drought classification
    if data.rainfall_mm < 500 or data.soil_moisture_percent < 20:
        drought_risk = "High"
    elif data.rainfall_mm < 800 or data.soil_moisture_percent < 35:
        drought_risk = "Moderate"
    else:
        drought_risk = "Low"

    # Extreme weather classification
    if data.temperature_c >= 40 or data.humidity_percent > 90:
        extreme_weather_risk = "High"
    elif data.temperature_c >= 35 or data.humidity_percent < 30:
        extreme_weather_risk = "Moderate"
    else:
        extreme_weather_risk = "Low"

    # Overall risk
    if score >= 60:
        overall_risk = "High"
        recommendation = (
            "Immediate irrigation and crop protection measures "
            "are recommended."
        )
    elif score >= 30:
        overall_risk = "Moderate"
        recommendation = (
            "Monitor soil moisture and weather conditions closely "
            "and plan irrigation if required."
        )
    else:
        overall_risk = "Low"
        recommendation = (
            "Current conditions are relatively safe. "
            "Continue regular crop monitoring."
        )

    return RiskAnalysisResponse(
        drought_risk=drought_risk,
        extreme_weather_risk=extreme_weather_risk,
        overall_risk=overall_risk,
        risk_score=round(score, 2),
        recommendation=recommendation,
    )