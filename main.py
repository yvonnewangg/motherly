import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

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
app_mode = st.sidebar.selectbox("Navigate", ["Home", "Weekly Screening", "Trends", "User Profile", "Chat", "Physician's Page"])

# Home Page (Log input)
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
                <h4 style='margin: 0;'>Log your symptoms</h4>
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

    # Navigation bar
    st.markdown(
        """
        <div style='position: fixed; bottom: 0; left: 0; right: 0; background-color: white; padding: 10px; display: flex; justify-content: space-around;'>
            <div>📅 Today</div>
            <div>📊 Insights</div>
            <div>📝 Screening</div>
            <div>💬 Chat</div>
            <div>👤 Profile</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Weekly Screening Page
elif app_mode == "Weekly Screening":
    st.title("Weekly Screening")
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
        ["No, not at all", "Hardly ever", "Yes, sometimes", "Yes, very often"],
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