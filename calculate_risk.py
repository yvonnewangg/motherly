import streamlit as st

# Define the weights for each factor
weights = {
    "mental_health_history": 0.25,
    "current_stress": 0.15,
    "social_support": 0.20,
    "physical_health": 0.10,
    "nutrition": 0.10,
    "sleep_quality": 0.10,
    "economic_stress": 0.05,
    "hormonal_changes": 0.05
}

# Function to calculate weighted score
def calculate_weighted_score(responses, weights):
    total_score = 0
    for factor, score in responses.items():
        total_score += score * weights[factor]
    return total_score

# App title
st.title("Personalized Postpartum Depression Risk Analyzer")

# Section 1: Edinburgh Postnatal Depression Scale (EPDS)
st.header("EPDS Score")
epds_score = st.slider("Enter your EPDS score (0-30):", 0, 30, 7)

# Section 2: User-Entered Risk Factors
st.header("PPD Risk Factors")

# 1. Feeling about Mental Health History
mental_health_history = st.selectbox(
    "How have you been feeling about your mental health lately?",
    ["Feeling good", "Some struggles", "Need support"]
)
mental_health_score = {"Feeling good": 3, "Some struggles": 6, "Need support": 10}[mental_health_history]

# 2. Current Stress Levels
current_stress = st.selectbox(
    "How are you managing stressors recently?",
    ["Low stress", "Moderate stress", "High stress"]
)
current_stress_score = {"Low stress": 3, "Moderate stress": 6, "High stress": 10}[current_stress]

# 3. Perception of Social Support
social_support = st.slider("How supported do you feel by friends and family (1-5)?", 1, 5, 3)
social_support_score = (6 - social_support) * 2  # Invert scale to reflect lack of support as higher risk

# 4. Physical Health Check-In
physical_health = st.selectbox(
    "How has your physical health been lately?",
    ["Feeling healthy", "Some concerns", "Need to see a doctor"]
)
physical_health_score = {"Feeling healthy": 3, "Some concerns": 6, "Need to see a doctor": 10}[physical_health]

# 5. Nutrition Check-In
nutrition = st.slider("How balanced were your meals this week (1-5)?", 1, 5, 3)
nutrition_score = (6 - nutrition) * 2  # Invert scale to reflect poor nutrition as higher risk

# 6. Sleep Quality Reflection
sleep_hours = st.slider("How many hours of sleep did you get on average this week?", 0, 12, 7)
sleep_quality = st.slider("How would you rate your sleep quality (1-5)?", 1, 5, 3)
sleep_score = (6 - sleep_quality) * 2  # Invert scale for poor sleep quality as higher risk

# 7. Economic Stress
economic_stress = st.slider("How are you feeling about your financial situation (1-5)?", 1, 5, 3)
economic_stress_score = economic_stress * 2

# 8. Hormonal Changes
hormonal_changes = st.selectbox(
    "Have you noticed any mood or physical changes due to hormones?",
    ["No", "Yes"]
)
hormonal_changes_score = {"No": 3, "Yes": 10}[hormonal_changes]

# Aggregate responses for calculation
responses = {
    "mental_health_history": mental_health_score,
    "current_stress": current_stress_score,
    "social_support": social_support_score,
    "physical_health": physical_health_score,
    "nutrition": nutrition_score,
    "sleep_quality": sleep_score,
    "economic_stress": economic_stress_score,
    "hormonal_changes": hormonal_changes_score
}

# Calculate overall risk score based on the weighted factors
weighted_risk_score = calculate_weighted_score(responses, weights)

# Final risk score adjustment by combining EPDS score and weighted risk score
total_risk_score = epds_score + weighted_risk_score

# Display personalized risk score
st.subheader("Your Personalized Postpartum Depression Risk Score")
st.write(f"EPDS Score: {epds_score}")
st.write(f"Weighted Risk Score (from additional factors): {weighted_risk_score:.2f}")
st.write(f"Total Risk Score: {total_risk_score:.2f}")

# Interpretation of the risk score based on EPDS thresholds
if total_risk_score <= 6:
    st.success("Low risk for postpartum depression.")
elif 7 <= total_risk_score <= 13:
    st.warning("Mild risk for postpartum depression. Consider consulting a physician.")
elif 14 <= total_risk_score <= 19:
    st.warning("Moderate risk for postpartum depression. Professional support is advised.")
else:
    st.error("High risk for postpartum depression. Seek immediate medical attention.")
