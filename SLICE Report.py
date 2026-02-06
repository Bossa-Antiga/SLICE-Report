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
# Programme setup
# -------------------------------------------------
st.header("⚙️ Programme Setup")

num_schools = st.number_input(
    "Number of schools",
    min_value=1,
    max_value=10,
    step=1,
    value=1
)

num_days = st.number_input(
    "Number of programme days (per school)",
    min_value=1,
    max_value=10,
    step=1,
    value=3
)

# -------------------------------------------------
# Data container
# -------------------------------------------------
all_schools_data = {}

# -------------------------------------------------
# School tabs
# -------------------------------------------------
school_tabs = st.tabs([f"School {i}" for i in range(1, num_schools + 1)])

for school_index, school_tab in enumerate(school_tabs, start=1):
    with school_tab:
        st.header(f"🏫 School {school_index} Information")

        school_name = st.text_input(
            "School Name",
            key=f"school_name_{school_index}"
        )

        teacher_name = st.text_input(
            "Teacher in Charge",
            key=f"teacher_name_{school_index}"
        )

        num_students = st.number_input(
            "Number of Students",
            min_value=0,
            step=1,
            key=f"num_students_{school_index}"
        )

        travel_rep = st.text_input(
            "Travel Agency Representative",
            key=f"travel_rep_{school_index}"
        )

        st.subheader("📜 Daily Reports")

        daily_data = {}

        # Day tabs inside school tab
        day_tabs = st.tabs([f"Day {d}" for d in range(1, num_days + 1)])

        for day, day_tab in enumerate(day_tabs, start=1):
            with day_tab:
                enthusiasm = st.select_slider(
                    "Student Enthusiasm",
                    options=["Low", "Average", "High"],
                    value="Average",
                    key=f"enthusiasm_{school_index}_{day}"
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
                    key=f"comments_{school_index}_{day}"
                )

                notes = st.text_area(
                    "Additional Notes",
                    key=f"notes_{school_index}_{day}"
                )

                daily_data[f"day_{day}"] = {
                    "enthusiasm": enthusiasm,
                    "comments": comments,
                    "notes": notes
                }

        all_schools_data[f"school_{school_index}"] = {
            "school_name": school_name,
            "teacher_name": teacher_name,
            "num_students": num_students,
            "travel_rep": travel_rep,
            "daily_data": daily_data
        }

# -------------------------------------------------
# Submit
# -------------------------------------------------
st.divider()

if st.button("✅ Submit All Reports"):
    rows = []

    for school_key, school in all_schools_data.items():
        if not school["school_name"] or not school["teacher_name"]:
            st.error("Each school must have a name and teacher.")
            st.stop()

        base_row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "school_name": school["school_name"],
            "teacher_name": school["teacher_name"],
            "num_students": school["num_students"],
            "travel_rep": school["travel_rep"],
            "num_days": num_days
        }

        for day in range(1, num_days + 1):
            base_row[f"day{day}_enthusiasm"] = school["daily_data"][f"day_{day}"]["enthusiasm"]
            base_row[f"day{day}_comments"] = school["daily_data"][f"day_{day}"]["comments"]
            base_row[f"day{day}_notes"] = school["daily_data"][f"day_{day}"]["notes"]

        rows.append(base_row)

    df = pd.DataFrame(rows)

    file_exists = os.path.isfile("reports.csv")
    df.to_csv("reports.csv", mode="a", header=not file_exists, index=False)

    st.success("🎉 All school reports submitted successfully!")
    st.balloons()
