# utils.py - Contains all health-related calculations

def calculate_bmi(weight, height):
    """Calculate Body Mass Index (BMI)."""
    return round(weight / (height ** 2), 2)

def classify_bmi(bmi):
    """Classify BMI into categories."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def calculate_lean_body_mass(weight, height, gender):
    """Calculate Lean Body Mass (LBM)."""
    if gender.lower() == "male":
        return round(0.407 * weight + 0.267 * height - 19.2, 2)
    else:
        return round(0.252 * weight + 0.473 * height - 48.3, 2)

def calculate_bmr(lean_body_mass):
    """Calculate Basal Metabolic Rate (BMR) using the Cunningham equation."""
    return round(500 + 22 * lean_body_mass, 2)

def calculate_met_score(weight, duration, intensity):
    """Calculate MET score based on activity intensity and duration."""
    MET_values = {"walking": 3.3, "moderate": 4, "vigorous": 8}
    return round(MET_values.get(intensity.lower(), 3.5) * weight * duration, 2)

def calculate_calories_burned(met_score, duration, weight):
    """Calculate calories burned during exercise."""
    return round(met_score * duration * weight, 2)

def classify_activity_level(met_minutes):
    """Classify physical activity level based on MET minutes per week."""
    if met_minutes < 600:
        return "Low"
    elif 600 <= met_minutes < 1500:
        return "Moderate"
    else:
        return "High"

def calculate_whr(waist, hip):
    """Calculate Waist-to-Hip Ratio (WHR)."""
    return round(waist / hip, 2)

def classify_whr(waist, hip, gender):
    """Classify Waist-to-Hip Ratio (WHR) into risk levels."""
    whr = calculate_whr(waist, hip)
    if gender.lower() == "male":
        if whr < 0.9: return "Low Risk"
        elif 0.9 <= whr <= 0.99: return "At Risk"
        else: return "High Risk"
    else:
        if whr < 0.8: return "Low Risk"
        elif 0.8 <= whr <= 0.89: return "At Risk"
        else: return "High Risk"

def calculate_tee(bmr, tea, tef):
    """Calculate Total Energy Expenditure (TEE)."""
    return round(bmr + tea + tef, 2)

def calculate_tef(tee):
    """Calculate Thermic Effect of Food (TEF) as 10% of TEE."""
    return round(0.1 * tee, 2)

def calculate_tea(met_score, weight):
    """Calculate Thermic Effect of Activity (TEA)."""
    return round(met_score * weight, 2)