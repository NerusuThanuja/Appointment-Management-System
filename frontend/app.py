import streamlit as st
import requests
import sqlite3

conn = sqlite3.connect("appointments.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Appointment Management System", layout="centered")

st.title("📅 Appointment Management System")

st.subheader("Create Appointment")

name = st.text_input("Name")
email = st.text_input("Email ID")
appointment_date = st.date_input("Appointment Date")
appointment_time = st.time_input("Appointment Time")

if st.button("Create Appointment"):
    if name and email:
        payload = {
            "name": name,
            "email": email,
            "appointment_date": str(appointment_date),
            "appointment_time": appointment_time.strftime("%I:%M %p")
        }

        response = requests.post(
            f"{BACKEND_URL}/appointments",
            json=payload
        )

        if response.status_code == 200:
            st.success("Appointment Created Successfully ✅")
        else:
            st.error("Failed to create appointment ❌")
    else:
        st.warning("Please fill all fields")

st.divider()

st.subheader("📋 All Appointments")

if st.button("View Appointments"):
    response = requests.get(f"{BACKEND_URL}/appointments")

    if response.status_code == 200:
        appointments = response.json()
        if appointments:
            for appt in appointments:
                st.write(
                    f"**NAME:** {appt['NAME']} | "
                    f"**EMAIL:** {appt['EMAIL']} | "
                    f"**DATE:** {appt['APPOINTMENT_DATE']} | "
                    f"**TIME:** {appt['APPOINTMENT_TIME']}"
                )
        else:
            st.info("No appointments found")
    else:
        st.error("Failed to fetch appointments")