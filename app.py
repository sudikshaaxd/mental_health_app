import streamlit as st
import pandas as pd
import joblib

# --- LOGIN SYSTEM ---
# Predefined credentials (you can change these)
USER_CREDENTIALS = {
    "admin": "1234",   # username: password
    "test": "pass"
}

# Session state to store login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

# --- MAIN APP ---
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
    # Load model
    model = joblib.load("model.pkl")

    st.title("🧠 Mental Health Risk Predictor")
    st.markdown("Answer the questions below to check mental health risk.")

if not st.session_state.logged_in:
    login()
else:
    # Load model
    model = joblib.load("model.pkl")

    st.title("🧠 Mental Health Risk Predictor")
    st.markdown("Answer the questions below to check mental health risk.")

    # Example input fields
    age = st.slider("Age", 18, 65, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    family_history = st.selectbox("Family history of mental illness?", ["Yes", "No"])

    # Create input data
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'family_history': [family_history]
    })

    if st.button("Predict Risk"):
        prediction = model.predict(input_data)[0]
        st.success("🔴 At Risk" if prediction else "🟢 Not at Risk")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

