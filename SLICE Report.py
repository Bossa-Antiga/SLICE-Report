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

# Folder for uploaded photos
UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

all_schools_data = {}

# -------------------------------------------------
# School tabs
# -------------------------------------------------
school_tabs = st.tabs([f"School {i}" for i in range(1, num_schools + 1)])

for school_index, school_tab in enumerate(school_tabs, start=1):
    with school_tab:
        st.header(f"🏫 School {school_index}")

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

        num_days = st.number_input(
            "Number of programme days for this school",
            min_value=1,
            max_value=10,
            step=1,
            value=3,
            key=f"num_days_{school_index}"
        )

        st.subheader("📜 Daily Reports")

        daily_data = {}

        day_tabs = st.tabs([f"Day {d}" for d in range(1, num_days + 1)])

        for day, day_tab in enumerate(day_tabs, start=1):
            with day_tab:
                enthusiasm = st.select_slider(
                    "Student Enthusiasm",
                    options=["Low", "Average", "High"],
                    value="Average",
                    key=f"enthusiasm_{school_index}_{day}"
                )

                 # --- Enthusiasm slider
    enthusiasm = st.select_slider(
        "Student Enthusiasm",
        options=["Low", "Average", "High"],
        value="Average",
        key=f"enthusiasm_{day}"
    )

    # --- Colour indicator under slider
    if enthusiasm == "Low":
        color = "#ff4b4b"
        text = "Low enthusiasm 😕"
    elif enthusiasm == "Average":
        color = "#f7d046"
        text = "Average enthusiasm 😐"
    else:
        color = "#2ecc71"
        text = "High enthusiasm 😄"

    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            margin-top: -10px;
            margin-bottom: 12px;
        ">
            <div style="
                background-color: {color};
                color: black;
                padding: 6px 16px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 0.9rem;
            ">
                {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

comments = st.text_area(
                    "Comments",
                    key=f"comments_{school_index}_{day}"
                )

notes = st.text_area(
                    "Additional Notes",
                    key=f"notes_{school_index}_{day}"
                )

photos = st.file_uploader(
                    "Attach photos (optional)",
                    type=["png", "jpg", "jpeg"],
                    accept_multiple_files=True,
                    key=f"photos_{school_index}_{day}"
                )

photo_names = []

                for photo in photos:
                    filename = f"{school_index}_day{day}_{photo.name}"
                    file_path = os.path.join(UPLOAD_DIR, filename)

                    with open(file_path, "wb") as f:
                        f.write(photo.getbuffer())

                    photo_names.append(filename)

                daily_data[f"day_{day}"] = {
                    "enthusiasm": enthusiasm,
                    "comments": comments,
                    "notes": notes,
                    "photos": "; ".join(photo_names)
                }

        all_schools_data[f"school_{school_index}"] = {
            "school_name": school_name,
            "teacher_name": teacher_name,
            "num_students": num_students,
            "travel_rep": travel_rep,
            "num_days": num_days,
            "daily_data": daily_data
        }

# -------------------------------------------------
# Submit
# -------------------------------------------------
st.divider()

if st.button("✅ Submit All Reports"):
    rows = []

    for school in all_schools_data.values():
        if not school["school_name"] or not school["teacher_name"]:
            st.error("Each school must have a name and teacher.")
            st.stop()

        base = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "school_name": school["school_name"],
            "teacher_name": school["teacher_name"],
            "num_students": school["num_students"],
            "travel_rep": school["travel_rep"],
            "num_days": school["num_days"]
        }

        for day_key, day_data in school["daily_data"].items():
            base[f"{day_key}_enthusiasm"] = day_data["enthusiasm"]
            base[f"{day_key}_comments"] = day_data["comments"]
            base[f"{day_key}_notes"] = day_data["notes"]
            base[f"{day_key}_photos"] = day_data["photos"]

        rows.append(base)

    df = pd.DataFrame(rows)

    file_exists = os.path.isfile("reports.csv")
    df.to_csv("reports.csv", mode="a", header=not file_exists, index=False)

    st.success("🎉 All reports submitted successfully!")
    st.balloons()
