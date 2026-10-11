# Smart Fertilizer Recommendation Engine

def recommend_fertilizer(crop, nitrogen, phosphorus, potassium, ph):
    """
    Gives a basic fertilizer recommendation based on
    crop and soil nutrient levels.

    Note:
    These are prototype threshold values.
    Later we will replace them with crop-specific
    agronomic recommendations / soil-test data.
    """

    recommendations = []

    # -----------------------------------------
    # Nitrogen
    # -----------------------------------------

    if nitrogen < 40:
        recommendations.append({
            "nutrient": "Nitrogen",
            "status": "Low",
            "recommendation": "Apply nitrogen-rich fertilizer"
        })

    elif nitrogen < 70:
        recommendations.append({
            "nutrient": "Nitrogen",
            "status": "Moderate",
            "recommendation": "Apply a moderate amount of nitrogen fertilizer"
        })

    else:
        recommendations.append({
            "nutrient": "Nitrogen",
            "status": "Adequate",
            "recommendation": "No major nitrogen deficiency detected"
        })

    # -----------------------------------------
    # Phosphorus
    # -----------------------------------------

    if phosphorus < 30:
        recommendations.append({
            "nutrient": "Phosphorus",
            "status": "Low",
            "recommendation": "Apply phosphorus-rich fertilizer"
        })

    elif phosphorus < 60:
        recommendations.append({
            "nutrient": "Phosphorus",
            "status": "Moderate",
            "recommendation": "Apply a moderate amount of phosphorus fertilizer"
        })

    else:
        recommendations.append({
            "nutrient": "Phosphorus",
            "status": "Adequate",
            "recommendation": "No major phosphorus deficiency detected"
        })

    # -----------------------------------------
    # Potassium
    # -----------------------------------------

    if potassium < 30:
        recommendations.append({
            "nutrient": "Potassium",
            "status": "Low",
            "recommendation": "Apply potassium-rich fertilizer"
        })

    elif potassium < 60:
        recommendations.append({
            "nutrient": "Potassium",
            "status": "Moderate",
            "recommendation": "Apply a moderate amount of potassium fertilizer"
        })

    else:
        recommendations.append({
            "nutrient": "Potassium",
            "status": "Adequate",
            "recommendation": "No major potassium deficiency detected"
        })

    # -----------------------------------------
    # Soil pH
    # -----------------------------------------

    if ph < 5.5:
        ph_status = "Acidic"
        ph_recommendation = "Consider soil-liming based on soil test"

    elif ph > 8.0:
        ph_status = "Alkaline"
        ph_recommendation = "Consider soil amendment based on soil test"

    else:
        ph_status = "Suitable"
        ph_recommendation = "pH is within a generally suitable range"

    return {
        "crop": crop,
        "soil_ph": ph,
        "ph_status": ph_status,
        "ph_recommendation": ph_recommendation,
        "nutrients": recommendations
    }


# -----------------------------------------
# Test
# -----------------------------------------

if __name__ == "__main__":

    result = recommend_fertilizer(
        crop="Rice",
        nitrogen=35,
        phosphorus=25,
        potassium=45,
        ph=6.5
    )

    print("====================================")
    print("   SMART FERTILIZER RECOMMENDATION")
    print("====================================")

    print("Crop:", result["crop"])
    print("Soil pH:", result["soil_ph"])
    print("pH Status:", result["ph_status"])
    print("pH Recommendation:", result["ph_recommendation"])

    print("------------------------------------")
    print("NUTRIENT ANALYSIS")
    print("------------------------------------")

    for item in result["nutrients"]:
        print(
            item["nutrient"],
            "|",
            item["status"],
            "|",
            item["recommendation"]
        )

    print("------------------------------------")