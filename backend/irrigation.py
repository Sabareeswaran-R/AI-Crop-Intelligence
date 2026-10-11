# Smart Irrigation Recommendation Engine

def recommend_irrigation(
    crop,
    area,
    soil_moisture,
    temperature,
    rainfall,
    growth_stage,
    soil_type,
    irrigation_method
):
    """
    Prototype smart irrigation recommendation.
    Later this can be upgraded with ET-based calculations,
    weather forecasts, soil sensors and crop-specific models.
    """

    # Soil moisture status
    if soil_moisture < 30:
        moisture_status = "Low"
    elif soil_moisture < 60:
        moisture_status = "Moderate"
    else:
        moisture_status = "Adequate"

    # Basic irrigation decision
    if rainfall >= 10:
        action = "No irrigation required"
        reason = "Sufficient rainfall is expected."
    elif soil_moisture < 30:
        action = "Irrigation required"
        reason = "Soil moisture is low."
    elif temperature >= 35 and soil_moisture < 45:
        action = "Light irrigation recommended"
        reason = "High temperature with relatively low soil moisture."
    else:
        action = "Monitor soil moisture"
        reason = "Current conditions do not indicate immediate irrigation need."

    return {
        "crop": crop,
        "area": area,
        "soil_moisture": soil_moisture,
        "moisture_status": moisture_status,
        "temperature": temperature,
        "expected_rainfall": rainfall,
        "growth_stage": growth_stage,
        "soil_type": soil_type,
        "irrigation_method": irrigation_method,
        "action": action,
        "reason": reason
    }


if __name__ == "__main__":

    result = recommend_irrigation(
        crop="Rice",
        area=2400,
        soil_moisture=25,
        temperature=34,
        rainfall=2,
        growth_stage="Vegetative",
        soil_type="Clay",
        irrigation_method="Drip"
    )

    print("====================================")
    print("     SMART IRRIGATION SYSTEM")
    print("====================================")
    print("Crop:", result["crop"])
    print("Field Area:", result["area"], "sqft")
    print("Soil Moisture:", result["soil_moisture"], "%")
    print("Moisture Status:", result["moisture_status"])
    print("Temperature:", result["temperature"], "°C")
    print("Expected Rainfall:", result["expected_rainfall"], "mm")
    print("Growth Stage:", result["growth_stage"])
    print("Soil Type:", result["soil_type"])
    print("Irrigation Method:", result["irrigation_method"])
    print("------------------------------------")
    print("ACTION:", result["action"])
    print("REASON:", result["reason"])
    print("------------------------------------")