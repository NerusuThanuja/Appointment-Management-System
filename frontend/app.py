import streamlit as st
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("appointments.db", check_same_thread=False)
cursor = conn.cursor()

# DROP OLD TABLE (fixes column mismatch error)
cursor.execute("DROP TABLE IF EXISTS appointments")

# CREATE FRESH TABLE
cursor.execute("""
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()

# ---------------- UI ----------------
st.set_page_config(page_title="Appointment Management System")
st.title("Appointment Management System")

st.subheader("Create Appointment")

name = st.text_input("Name")
email = st.text_input("Email ID")
appointment_date = st.date_input("Appointment Date")
appointment_time = st.time_input("Appointment Time")

# ---------------- CREATE APPOINTMENT ----------------
if st.button("Create Appointment"):
    if not name or not email:
        st.error("Please enter all details")
    else:
        cursor.execute(
            """
            SELECT * FROM appointments
            WHERE email = ? AND date = ? AND time = ?
            """,
            (email.upper(), str(appointment_date), str(appointment_time))
        )
        existing = cursor.fetchone()

        if existing:
            st.warning("Duplicate appointment not allowed")
        else:
            cursor.execute(
                """
                INSERT INTO appointments (name, email, date, time)
                VALUES (?, ?, ?, ?)
                """,
                (
                    name.upper(),
                    email.upper(),
                    str(appointment_date),
                    str(appointment_time)
                )
            )
            conn.commit()
            st.success("Appointment created successfully")

# ---------------- VIEW APPOINTMENTS ----------------
st.divider()
st.subheader("All Appointments")

cursor.execute(
    "SELECT name, email, date, time FROM appointments ORDER BY date, time"
)
appointments = cursor.fetchall()

if appointments:
    for appt in appointments:
        st.write(
            f"NAME: {appt[0]} | EMAIL: {appt[1]} | DATE: {appt[2]} | TIME: {appt[3]}"
        )
else:
    st.info("No appointments found")