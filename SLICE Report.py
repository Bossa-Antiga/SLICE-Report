import streamlit as st
import requests
from datetime import datetime
import os

# -------------------------------------------------
# GOOGLE SHEETS WEBHOOK
# -------------------------------------------------
WEBHOOK_URL = "YOUR_GOOGLE_APPS_SCRIPT_WEBHOOK_URL"

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="School Workshop Report",
    layout="centered"
)

st.title("SLICE Report")

# -------------------------------------------------
# PROGRAMME SETUP
# -------------------------------------------------
st.header("⚙️ Programme Setup")

num_schools = st.number_input(
    "Number of schools",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------------------------
# SCHOOL TABS
# -------------------------------------------------
school_tabs = st.tabs(
    [f"School {i}" for i in range(1, num_schools + 1)]
)

for school_index, school_tab in enumerate(school_tabs, start=1):

    with school_tab:

        st.header(f"🏫 School {school_index}")

        # -------------------------------------------------
        # SCHOOL INFO
        # -------------------------------------------------
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
            value=3,
            step=1,
            key=f"num_days_{school_index}"
        )

        st.subheader("📜 Daily Reports")

        # -------------------------------------------------
        # DAY TABS
        # -------------------------------------------------
        day_tabs = st.tabs(
            [f"Day {d}" for d in range(1, num_days + 1)]
        )

        all_day_data = []

        for day, day_tab in enumerate(day_tabs, start=1):

            with day_tab:

                # -------------------------------------------------
                # ENTHUSIASM SLIDER
                # -------------------------------------------------
                enthusiasm = st.select_slider(
                    "Student Enthusiasm",
                    options=["Low", "Average", "High"],
                    value="Average",
                    key=f"enthusiasm_{school_index}_{day}"
                )

                # -------------------------------------------------
                # COLOUR INDICATOR
                # -------------------------------------------------
                if enthusiasm == "Low":
                    color = "#ff4b4b"
                    text = "😕"

                elif enthusiasm == "Average":
                    color = "#f7d046"
                    text = "😐"

                else:
                    color = "#2ecc71"
                    text = "😄"

                st.markdown(
                    f"""
                    <div style="
                        display: flex;
                        justify-content: center;
                        margin-top: -10px;
                        margin-bottom: 15px;
                    ">
                        <div style="
                            background-color: {color};
                            padding: 6px 20px;
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

                # -------------------------------------------------
                # COMMENTS + NOTES
                # -------------------------------------------------
                comments = st.text_area(
                    "Comments",
                    key=f"comments_{school_index}_{day}"
                )

                notes = st.text_area(
                    "Additional Notes",
                    key=f"notes_{school_index}_{day}"
                )

                # -------------------------------------------------
                # PHOTO UPLOAD
                # -------------------------------------------------
                photos = st.file_uploader(
                    "Attach photos (optional)",
                    type=["png", "jpg", "jpeg"],
                    accept_multiple_files=True,
                    key=f"photos_{school_index}_{day}"
                )

                photo_names = []

                if photos:

                    for photo in photos:

                        filename = (
                            f"{school_index}_day{day}_{photo.name}"
                        )

                        filepath = os.path.join(
                            UPLOAD_DIR,
                            filename
                        )

                        with open(filepath, "wb") as f:
                            f.write(photo.getbuffer())

                        photo_names.append(filename)

                # -------------------------------------------------
                # STORE DAY DATA
                # -------------------------------------------------
                all_day_data.append({
                    "Day": f"Day {day}",
                    "Enthusiasm": enthusiasm,
                    "Comments": comments,
                    "Notes": notes,
                    "Photos": "; ".join(photo_names)
                })

        # -------------------------------------------------
        # SUBMIT BUTTON
        # -------------------------------------------------
        st.divider()

        if st.button(
            f"📤 Submit School {school_index}",
            key=f"submit_btn_{school_index}"
        ):

            if not school_name or not teacher_name:

                st.error(
                    "School name and teacher are required."
                )

            else:

                try:

                    # -------------------------------------------------
                    # SEND EACH DAY AS A NEW ROW
                    # -------------------------------------------------
                    for day_data in all_day_data:

                        row = {
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "School Name": school_name,
                            "Teacher Name": teacher_name,
                            "Number of Students": num_students,
                            "Travel Rep": travel_rep,
                            "Day": day_data["Day"],
                            "Enthusiasm": day_data["Enthusiasm"],
                            "Comments": day_data["Comments"],
                            "Notes": day_data["Notes"],
                            "Photos": day_data["Photos"]
                        }

                        requests.post(
                            WEBHOOK_URL,
                            json=row
                        )

                    st.success(
                        f"🎉 School {school_index} submitted successfully!"
                    )

                except Exception as e:

                    st.error(
                        "❌ Failed to send data to Google Sheets."
                    )

                    st.write(str(e))
