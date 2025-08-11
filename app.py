import streamlit as st
import joblib
import numpy as np

# --- USER CREDENTIALS ---
USER_CREDENTIALS = {
    "admin": "password123",  # Change this!
}

# --- LOGIN FUNCTION ---
def login():
    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- MAIN APP ---
if not st.session_state.logged_in:
    login()
else:
    # Load trained model
    model = joblib.load("model.pkl")

    st.title("🧠 Mental Health Risk Predictor")
    st.markdown("Answer the questions below to check your mental health risk.")

    # Form inputs
    age = st.number_input("Age", min_value=0, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    family_history = st.selectbox("Family History of Mental Illness?", ["Yes", "No"])
    work_interfere = st.selectbox("Does work interfere with your mental health?", ["Never", "Rarely", "Sometimes", "Often"])
    no_employees = st.selectbox("Number of Employees in Company", ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"])
    remote_work = st.selectbox("Do you work remotely?", ["Yes", "No"])
    tech_company = st.selectbox("Is it a tech company?", ["Yes", "No"])
    benefits = st.selectbox("Does your employer provide mental health benefits?", ["Yes", "No", "Don't know"])
    care_options = st.selectbox("Are care options available?", ["Yes", "No", "Not sure"])
    wellness_program = st.selectbox("Wellness program available?", ["Yes", "No", "Don't know"])
    seek_help = st.selectbox("Is help-seeking encouraged?", ["Yes", "No", "Don't know"])

    # Prediction
    if st.button("Predict Risk"):
        input_data = [[age, gender, family_history, work_interfere, no_employees,
                       remote_work, tech_company, benefits, care_options,
                       wellness_program, seek_help]]
        
        prediction = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0]

        risk_label = "High Risk" if prediction == 1 else "Low Risk"
        confidence = round(proba[prediction] * 100, 2)

        st.subheader(f"🩺 Prediction: {risk_label}")
        st.write(f"Confidence: **{confidence}%**")

        if prediction == 1:
            st.warning("⚠️ Consider seeking professional advice or support.")
        else:
            st.success("✅ You appear at low risk based on the information provided.")
