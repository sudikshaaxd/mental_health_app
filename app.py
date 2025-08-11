import streamlit as st
import joblib

# Dummy user credentials
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "mypassword"
}

# Initialize session state
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

    # Example inputs — replace with your actual form
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    stress_level = st.slider("Stress Level", 0, 10, 5)

    if st.button("Predict"):
        # Example prediction (replace with your model logic)
        prediction = model.predict([[age, stress_level]])[0]
        st.write(f"Predicted Risk: **{prediction}**")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
