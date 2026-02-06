import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="School Workshop Report",
    layout="centered"
)

st.title("SLICE Report")

# -------------------------------------------------
# School Information
# -------------------------------------------------
st.header("🏫 School Information")

school_name = st.text_input("School Name")
teacher_name = st.text_input("Teacher in Charge")
num_students = st.number_input("Number of Students", min_value=0, step=1)
travel_rep = st.text_input("Travel Agency Representative")

# -------------------------------------------------
# Programme setup
# -------------------------------------------------
st.header("🗓 Programme Days")

num_days = st.number_input(
    "Number of programme days",
    min_value=1,
    max_value=10,
    step=1,
    value=3
)

# -------------------------------------------------
# Daily Reports (TABS)
# -------------------------------------------------
st.header("📜 Daily Reports")

daily_data = {}

day_tabs = st.tabs([f"Day {i}" for i in range(1, num_days + 1)])

for day, tab in enumerate(day_tabs, start=1):
    with tab:
        enthusiasm = st.select_slider(
            "Student Enthusiasm",
            options=["Low", "Average", "High"],
            value="Average",
            key=f"enthusiasm_{day}"
        )

        # Colour feedback box
        if enthusiasm == "Low":
            st.error("Enthusiasm: Low 😕")
        elif enthusiasm == "Average":
            st.warning("Enthusiasm: Average 😐")
        else:
            st.success("Enthusiasm: High 😄")

        comments = st.text_area(
            "Comments",
            key=f"comments_{day}"
        )

        notes = st.text_area(
            "Additional Notes",
            key=f"notes_{day}"
        )

        daily_data[f"day_{day}"] = {
            "enthusiasm": enthusiasm,
            "comments": comments,
            "notes": notes
        }

# -------------------------------------------------
# Submit
# -------------------------------------------------
if st.button("✅ Submit Report"):

    if not school_name or not teacher_name:
        st.error("Please fill in at least the school name and teacher name.")
    else:
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "school_name": school_name,
            "teacher_name": teacher_name,
            "num_students": num_students,
            "travel_rep": travel_rep,
            "num_days": num_days
        }

        # Flatten day data for CSV
        for day in range(1, num_days + 1):
            report[f"day{day}_enthusiasm"] = daily_data[f"day_{day}"]["enthusiasm"]
            report[f"day{day}_comments"] = daily_data[f"day_{day}"]["comments"]
            report[f"day{day}_notes"] = daily_data[f"day_{day}"]["notes"]

        df = pd.DataFrame([report])

        file_exists = os.path.isfile("reports.csv")
        df.to_csv("reports.csv", mode="a", header=not file_exists, index=False)

        st.success("🎉 Report submitted successfully!")
        st.balloons()
