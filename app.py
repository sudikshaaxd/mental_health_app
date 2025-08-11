import streamlit as st
import joblib
import pandas as pd

# --- USER CREDENTIALS ---
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "mypassword"
}

# --- INITIALIZE SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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

# --- MAIN APP ---
if not st.session_state.logged_in:
    login()
else:
    # Load the trained model
    model = joblib.load("model.pkl")

    st.title("🧠 Mental Health Risk Predictor")
    st.markdown("Answer the questions below to check mental health risk.")

    # Input form for the 11 features
    age = st.number_input("Age", min_value=10, max_value=100, value=25)

    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    gender_map = {"Male": 0, "Female": 1, "Other": 2}

    family_history = st.selectbox("Family history of mental illness?", ["Yes", "No"])
    binary_map = {"No": 0, "Yes": 1}

    work_interfere = st.selectbox(
        "Does your mental health interfere with work?",
        ["Never", "Rarely", "Sometimes", "Often"]
    )
    work_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3}

    no_employees = st.selectbox(
        "Number of employees",
        ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
    )
    emp_map = {
        "1-5": 0, "6-25": 1, "26-100": 2,
        "100-500": 3, "500-1000": 4, "More than 1000": 5
    }

    remote_work = st.selectbox("Do you work remotely?", ["Yes", "No"])
    tech_company = st.selectbox("Do you work in a tech company?", ["Yes", "No"])

    benefits = st.selectbox(
        "Does your employer provide mental health benefits?",
        ["Yes", "No", "Don't know"]
    )
    care_options = st.selectbox(
        "Are you aware of care options provided by your employer?",
        ["Yes", "No", "Not sure"]
    )
    wellness_program = st.selectbox(
        "Does your employer have a wellness program?",
        ["Yes", "No", "Don't know"]
    )
    seek_help = st.selectbox(
        "Does your employer encourage seeking help for mental health?",
        ["Yes", "No", "Don't know"]
    )

    if st.button("Predict"):
        # Create DataFrame in the correct order
        input_data = pd.DataFrame([[
            age,
            gender_map[gender],
            binary_map[family_history],
            work_map[work_interfere],
            emp_map[no_employees],
            binary_map[remote_work],
            binary_map[tech_company],
            {"Yes": 1, "No": 0, "Don't know": 2}[benefits],
            {"Yes": 1, "No": 0, "Not sure": 2}[care_options],
            {"Yes": 1, "No": 0, "Don't know": 2}[wellness_program],
            {"Yes": 1, "No": 0, "Don't know": 2}[seek_help]
        ]], columns=[
            'Age', 'Gender', 'family_history', 'work_interfere', 'no_employees',
            'remote_work', 'tech_company', 'benefits', 'care_options',
            'wellness_program', 'seek_help'
        ])

        # Predict
        prediction = model.predict(input_data)[0]
        st.write(f"Predicted Risk: **{prediction}**")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
