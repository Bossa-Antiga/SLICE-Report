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

# Daily Reports

st.header("📜 Daily Reports")

daily_data = {}

for day in range(1, 4):
    st.subheader(f"Day {day}")

    enthusiasm = st.select_slider(
        "Student Enthusiasm",
        options=["Low", "Average", "High"],
        value="Average",
        key=f"enthusiasm_{day}"
    )

    if enthusiasm == "Low":
        st.error("🔴")
    elif enthusiasm == "Average":
        st.warning("🟡")
    else:
        st.success("🟢")

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


enthusiasm = st.select_slider(
    "Student Enthusiasm",
    options=[
        "Very Low",
        "Low",
        "Average",
        "High",
        "Very High"
    ],
    value="Average"
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
        
