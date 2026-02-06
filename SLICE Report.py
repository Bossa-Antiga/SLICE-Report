# @title

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="School Workshop Report", layout="centered")

st.title("SLICE Report")


# School Information

st.header("🏫 School Information")

school_name = st.text_input("School Name")
teacher_name = st.text_input("Teacher in Charge")
num_students = st.number_input("Number of Students", min_value=0, step=1)
travel_rep = st.text_input("Travel Agency Representative")


# Daily Reports

st.header("📜 Daily Reports")

daily_data = {}

for day in range(1, 4):
    st.subheader(f"Day {day}")

   enthusiasm_value = st.slider(
    "Student Enthusiasm",
    min_value=1,
    max_value=5,
    value=3,
    key=f"enthusiasm_{day}"
)

enthusiasm_map = {
    1: "Very Low",
    2: "Low",
    3: "Average",
    4: "High",
    5: "Very High"
}

enthusiasm = enthusiasm_map[enthusiasm_value]
if enthusiasm_value in [1, 2]:
    slider_color = "#e74c3c"   # red
elif enthusiasm_value == 3:
    slider_color = "#f1c40f"   # yellow
else:
    slider_color = "#2ecc71"   # green
st.markdown(
    f"""
    <style>
    div[data-baseweb="slider"] > div > div > div {{
        background-color: {slider_color} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


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

# Submit Button

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

            "day1_enthusiasm": daily_data["day_1"]["enthusiasm"],
            "day1_comments": daily_data["day_1"]["comments"],
            "day1_notes": daily_data["day_1"]["notes"],

            "day2_enthusiasm": daily_data["day_2"]["enthusiasm"],
            "day2_comments": daily_data["day_2"]["comments"],
            "day2_notes": daily_data["day_2"]["notes"],

            "day3_enthusiasm": daily_data["day_3"]["enthusiasm"],
            "day3_comments": daily_data["day_3"]["comments"],
            "day3_notes": daily_data["day_3"]["notes"],
        }

        df = pd.DataFrame([report])

        file_exists = os.path.isfile("reports.csv")
        df.to_csv("reports.csv", mode="a", header=not file_exists, index=False)

        st.success("🎉 Report submitted successfully!")
        st.balloons()
        
