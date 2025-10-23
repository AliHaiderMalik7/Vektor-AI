def normalize_and_bmi(weight_value, weight_unit, height_value, height_unit, height_extra_inches = None):
    
    # Converting weight unit lbs to kg
    if weight_unit.lower() == "lbs":
        weight_kg = weight_value * 0.453592
    else:
        weight_kg = weight_value

    if height_unit.lower() == "cm":
        height_cm = height_value
    else:
        # assume height_value is feet, and height_extra_inches given
        total_inches = height_value * 12 + (height_extra_inches or 0)
        height_cm = total_inches * 2.54 
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 2)

    if bmi < 18.5:
        cat = "Underweight"
    elif bmi < 25:
        cat = "Normal"
    elif bmi < 30:
        cat = "Overweight"
    else:
        cat = "Obese"

    return {
        "normalized_weight_kg": round(weight_kg, 2),
        "normalized_height_cm": round(height_cm, 1),
        "bmi": bmi,
        "bmi_category": cat
    }