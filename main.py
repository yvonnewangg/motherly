import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Sample data for trend analysis
sample_data = {
    "Date": pd.date_range(start="2024-09-01", periods=7, freq="D"),
    "Mental Health Score": np.random.randint(1, 10, 7),
    "Stress Score": np.random.randint(1, 10, 7),
    "Social Support Score": np.random.randint(1, 5, 7),
    "Physical Health Score": np.random.randint(1, 10, 7),
    "Nutrition Score": np.random.randint(1, 5, 7),
    "Sleep Score": np.random.randint(1, 5, 7),
    "EPDS Score": np.random.randint(7, 19, 7),
}

# Convert sample data to DataFrame
df = pd.DataFrame(sample_data)

# Sidebar Navigation
st.sidebar.title("Postpartum Health App")
app_mode = st.sidebar.selectbox("Navigate", ["Home", "Trends", "User Profile", "Chat", "Physician's Page"])

# Home Page (Log input and Weekly Screening)
if app_mode == "Home":
    st.title("Postpartum Health Tracker")
    
    # Display current date
    current_date = datetime.date.today()
    st.subheader(current_date.strftime("%B %d"))

    # Calendar-like date picker
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    weekdays = ["S", "M", "T", "W", "T", "F", "S"]
    for i, day in enumerate(range(current_date.day - 3, current_date.day + 4)):
        cols = [col1, col2, col3, col4, col5, col6, col7]
        with cols[i]:
            st.write(weekdays[i])
            if day == current_date.day:
                st.button(str(day), key=f"day_{day}", disabled=True)
            else:
                st.button(str(day), key=f"day_{day}")

    # Days since delivery tracker
    st.markdown("### Days since delivery")
    st.markdown("## 42 days")
    st.button("Update delivery date")

    # New feature or tip
    st.markdown(
        """
        <div style='background: linear-gradient(to right, #FFA07A, #DA70D6); padding: 10px; border-radius: 10px;'>
            <h4 style='color: white; margin: 0;'>Tip of the day</h4>
            <h3 style='color: white; margin: 0;'>Self-care is important!</h3>
            <p style='color: white; margin: 0;'>Take 10 minutes for yourself today 💆‍♀️</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Daily insights
    st.markdown("### My daily check-in")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px;'>
                <h4 style='color: #FF69B4; style: 'margin: 0;'>Log your symptoms</h4>
                <h1 style='color: #FF69B4; font-size: 48px; margin: 0;'>+</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='background-color: #FFB6C1; padding: 10px; border-radius: 10px;'>
                <p style='margin: 0;'>Your weekly screening is due. Click here to take it.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Log symptoms (hidden by default, can be expanded)
    with st.expander("Log your daily check-in"):
        # Mental Health
        st.subheader("Mental Health")
        mental_health = st.select_slider(
            "How have you been feeling about your mental health today?",
            options=["Need support", "Some struggles", "Feeling good"]
        )
        st.text_area("Add any details about your mental health:")

        # Stress Levels
        st.subheader("Stress Levels")
        stress = st.select_slider(
            "Have you experienced any significant stressors today?",
            options=["Low stress", "Moderate stress", "High stress"]
        )
        st.text_area("Add any details about your stress:")

        # Social Support
        st.subheader("Social Support")
        social_support = st.slider("How supported do you feel by friends and family today? (1-5)", 1, 5)

        # Physical Health
        st.subheader("Physical Health")
        physical_health = st.select_slider(
            "How has your physical health been today?",
            options=["Need to see a doctor", "Some concerns", "Feeling healthy"]
        )

        # Nutrition
        st.subheader("Nutrition")
        nutrition = st.slider("How balanced were your meals today? (1-5)", 1, 5)
        st.text_area("Add any details about your nutrition:")

        # Sleep Quality
        st.subheader("Sleep Quality")
        sleep_hours = st.slider("How many hours of sleep did you get last night?", 0, 12)
        sleep_quality = st.slider("How would you rate your sleep quality? (1-5)", 1, 5)

        # Economic Stress
        st.subheader("Economic Stress")
        economic_stress = st.slider("How are you feeling about your financial situation today? (1-5)", 1, 5)

        # Hormonal Changes
        st.subheader("Hormonal Changes")
        hormonal_changes = st.selectbox(
            "Have you noticed any mood or physical changes that might be hormonal?",
            ["No", "Yes"]
        )
        if hormonal_changes == "Yes":
            st.text_area("Please describe the changes:")

        # Log Data
        if st.button("Log Today's Data"):
            st.success("Your data has been logged for today!")

    # Weekly Screening
    st.markdown("### Weekly Screening")
    st.subheader("Edinburgh Postnatal Depression Scale (EPDS)")

    # EPDS Test
    epds_questions = [
        "I have been able to laugh and see the funny side of things",
        "I have looked forward with enjoyment to things",
        "I have blamed myself unnecessarily when things went wrong",
        "I have been anxious or worried for no good reason",
        "I have felt scared or panicky for no good reason",
        "Things have been getting to me",
        "I have been so unhappy that I have had difficulty sleeping",
        "I have felt sad or miserable",
        "I have been so unhappy that I have been crying",
        "The thought of harming myself has occurred to me"
    ]

    epds_options = [
        ["As much as I always could", "Not quite so much now", "Definitely not so much now", "Not at all"],
        ["As much as I ever did", "Rather less than I used to", "Definitely less than I used to", "Hardly at all"],
        ["Yes, most of the time", "Yes, some of the time", "Not very often", "No, never"],
        ["Yes, very often", "Yes, sometimes", "Hardly ever", "No, not at all"],
        ["Yes, quite a lot", "Yes, sometimes", "No, not much", "No, not at all"],
        ["Yes, most of the time I haven't been able to cope at all", "Yes, sometimes I haven't been coping as well as usual", "No, most of the time I have coped quite well", "No, I have been coping as well as ever"],
        ["Yes, most of the time", "Yes, sometimes", "Not very often", "No, not at all"],
        ["Yes, most of the time", "Yes, quite often", "Not very often", "No, not at all"],
        ["Yes, most of the time", "Yes, quite often", "Only occasionally", "No, never"],
        ["Yes, quite often", "Sometimes", "Hardly ever", "Never"]
    ]

    epds_score = 0

    for i, (question, options) in enumerate(zip(epds_questions, epds_options)):
        answer = st.radio(question, options, key=f"epds_{i}")
        if i in [0, 1]:  # Questions 1 and 2 are scored normally
            epds_score += options.index(answer)
        else:  # The rest are reverse scored
            epds_score += 3 - options.index(answer)

    st.subheader(f"Your EPDS Score: {epds_score}")

    if epds_score <= 9:
        st.success("Your score indicates a low risk for postpartum depression.")
    elif 10 <= epds_score <= 12:
        st.warning("Your score indicates a possible risk for postpartum depression. Consider discussing this with your healthcare provider.")
    else:
        st.error("Your score indicates a high risk for postpartum depression. We strongly recommend contacting your healthcare provider for further evaluation and support.")

    # Calculate Risk Logic
    st.header("Risk Score Analyzer")

    # Define the weights for each factor
    weights = {
        "mental_health": 0.25,
        "stress": 0.15,
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

    # Aggregate responses for calculation
    responses = {
        "mental_health": {"Need support": 10, "Some struggles": 6, "Feeling good": 3}[mental_health],
        "stress": {"Low stress": 3, "Moderate stress": 6, "High stress": 10}[stress],
        "social_support": (6 - social_support) * 2,  # Invert scale to reflect lack of support as higher risk
        "physical_health": {"Need to see a doctor": 10, "Some concerns": 6, "Feeling healthy": 3}[physical_health],
        "nutrition": (6 - nutrition) * 2,  # Invert scale to reflect poor nutrition as higher risk
        "sleep_quality": (6 - sleep_quality) * 2,  # Invert scale for poor sleep quality as higher risk
        "economic_stress": economic_stress * 2,  # Direct score for economic stress
        "hormonal_changes": {"No": 3, "Yes": 10}[hormonal_changes]
    }

    # Calculate overall risk score based on the weighted factors
    weighted_risk_score = calculate_weighted_score(responses, weights)

    # Final risk score adjustment by combining EPDS score and weighted risk score
    total_risk_score = epds_score + weighted_risk_score

    # Display personalized risk score
    st.subheader("Your Personalized Risk Score")
    st.write(f"EPDS Score: {epds_score}")
    st.write(f"Weighted Risk Score (from daily check-in factors): {weighted_risk_score:.2f}")
    st.write(f"Total Risk Score: {total_risk_score:.2f}")

        # Explanation of Risk Scores
    st.markdown("""
    ### Understanding Your Risk Scores

    - **EPDS Score**: This score is derived from the Edinburgh Postnatal Depression Scale, which assesses the risk of postpartum depression.
        - **0-9**: Low risk for postpartum depression
        - **10-12**: Possible risk; consider discussing this with your healthcare provider
        - **13 or higher**: High risk; strong recommendation to contact your healthcare provider for further evaluation

    - **Personalized Risk Score**: Your total risk score combines your EPDS score and your daily logged answers, providing a comprehensive view of your well-being. The maximum possible score is **40**. 

        - **0-10**: Low overall risk; generally managing well
        - **11-20**: Moderate risk; some areas may need attention
        - **21-30**: High risk; consider reaching out for additional support
        - **31-40**: Very high risk; immediate professional assistance is advised

    This personalized score helps you and your healthcare provider identify areas where you may need extra support and track your mental health over time.
    """)

    # Display personalized risk score
    st.subheader("Your Personalized Risk Score")
    
    # Interpretation of the risk score based on thresholds
    if total_risk_score <= 6:
        st.success("Low risk for postpartum depression.")
    elif 7 <= total_risk_score <= 13:
        st.warning("Mild risk for postpartum depression. Consider consulting a physician.")
    elif 14 <= total_risk_score <= 19:
        st.warning("Moderate risk for postpartum depression. Professional support is advised.")
    else:
        st.error("High risk for postpartum depression. Seek immediate medical attention.")

# Trend Page
elif app_mode == "Trends":
    st.title("Trends - View Historical Data")
    
    # Plot historical data for mental health and other metrics
    st.line_chart(df.set_index("Date"))

    st.subheader("Historical Data Overview")
    st.write(df)

# User Profile Page
elif app_mode == "User Profile":
    st.title("User Profile")

    # Example profile info (could be retrieved from a database in a real app)
    st.subheader("User Information")
    st.write("Name: Jane Doe")
    st.write("Age: 32")
    st.write("Weeks Postpartum: 6")
    st.write("Email: janedoe@example.com")

    # Update Profile Info
    st.subheader("Update Your Profile")
    new_name = st.text_input("Name", value="Jane Doe")
    new_email = st.text_input("Email", value="janedoe@example.com")
    new_weeks_postpartum = st.number_input("Weeks Postpartum", value=6, min_value=0)
    if st.button("Update Profile"):
        st.success("Your profile has been updated!")

# Chat Page
elif app_mode == "Chat":
    st.title("Chat with Your Healthcare Provider")
    
    st.write("This is a placeholder for the chat functionality. In a full implementation, you would integrate a secure messaging system here.")
    
    message = st.text_input("Type your message here:")
    if st.button("Send"):
        st.success("Message sent to your healthcare provider!")

# Physician's Page
elif app_mode == "Physician's Page":
    st.title("Physician's Page - Monitor Patients")

    st.subheader("Key Patient Metrics")

    # Display summary metrics for physician review
    st.write("Patient: Jane Doe")
    st.write("Weeks Postpartum: 6")
    st.write("Latest EPDS Score: 8")
    st.write("Average Sleep This Week: 7 hours")
    st.write("Average Sleep Quality: 4/5")
    st.write("Average Stress Level: 3/5")

    # Show patient's trends
    st.subheader("Patient's Data Trends")
    st.line_chart(df.set_index("Date"))
    
    # Example: Send feedback to patient
    st.subheader("Send Feedback to Patient")
    feedback = st.text_area("Enter your feedback here:")
    if st.button("Send Feedback"):
        st.success("Feedback sent to the patient.")

    # Appointment Scheduling
    st.subheader("Schedule Appointment")
    appointment_date = st.date_input("Select appointment date")
    appointment_time = st.time_input("Select appointment time")
    if st.button("Schedule Appointment"):
        st.success(f"Appointment scheduled for {appointment_date} at {appointment_time}")
