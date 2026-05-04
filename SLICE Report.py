import streamlit as st
import requests
from datetime import datetime
import os

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbySK0gEBBqWnAQP_PTgygm5aQQCusSMk2HXciXkDvleeETyw3EGZP1dCF5sRJaKI5NUiA/exec"

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

UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------------------------
# School Tabs
# -------------------------------------------------
school_tabs = st.tabs([f"School {i}" for i in range(1, num_schools + 1)])

for school_index, school_tab in enumerate(school_tabs, start=1):

    with school_tab:

        st.header(f"🏫 School {school_index}")

        # -------------------------------------------------
        # School Information
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
        # Day Tabs
        # -------------------------------------------------
        day_tabs = st.tabs(
            [f"Day {d}" for d in range(1, num_days + 1)]
        )

        for day, day_tab in enumerate(day_tabs, start=1):

            with day_tab:

                # -------------------------------------------------
                # Enthusiasm Slider
                # -------------------------------------------------
                enthusiasm = st.select_slider(
                    "Student Enthusiasm",
                    options=["Low", "Average", "High"],
                    value="Average",
                    key=f"enthusiasm_{school_index}_{day}"
                )

                # -------------------------------------------------
                # Colour Indicator
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
                # Comments
                # -------------------------------------------------
                st.text_area(
                    "Comments",
                    key=f"comments_{school_index}_{day}"
                )

                st.text_area(
                    "Additional Notes",
                    key=f"notes_{school_index}_{day}"
                )

                # -------------------------------------------------
                # Photo Upload
                # -------------------------------------------------
                photos = st.file_uploader(
                    "Attach photos (optional)",
                    type=["png", "jpg", "jpeg"],
                    accept_multiple_files=True,
                    key=f"photos_{school_index}_{day}"
                )

                if photos:
                    for photo in photos:

                        filename = f"{school_index}_day{day}_{photo.name}"
                        filepath = os.path.join(UPLOAD_DIR, filename)

                        with open(filepath, "wb") as f:
                            f.write(photo.getbuffer())

        # -------------------------------------------------
        # Submit Buttons
        # -------------------------------------------------
        submit_key = f"submit_clicked_{school_index}"
        confirm_key = f"confirm_submit_{school_index}"
        submitted_key = f"submitted_{school_index}"

        if submit_key not in st.session_state:
            st.session_state[submit_key] = False

        if confirm_key not in st.session_state:
            st.session_state[confirm_key] = False

        if submitted_key not in st.session_state:
            st.session_state[submitted_key] = False

        st.divider()

        # -------------------------------------------------
        # Already Submitted
        # -------------------------------------------------
        if st.session_state[submitted_key]:

            st.success("✅ This school has already been submitted.")

        else:

            # -------------------------------------------------
            # Initial Submit Button
            # -------------------------------------------------
            if st.button(
                f"📤 Submit School {school_index}",
                key=f"submit_btn_{school_index}"
            ):
                st.session_state[submit_key] = True

            # -------------------------------------------------
            # Confirmation Prompt
            # -------------------------------------------------
            if st.session_state[submit_key]:

                st.warning(
                    "Are you sure you want to submit this school report?"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✔ Confirm Save",
                        key=f"confirm_btn_{school_index}"
                    ):
                        st.session_state[confirm_key] = True

                with col2:

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_btn_{school_index}"
                    ):
                        st.session_state[submit_key] = False
                        st.session_state[confirm_key] = False
                        st.rerun()

            # -------------------------------------------------
            # Final Submission
            # -------------------------------------------------
            if st.session_state[confirm_key]:

                if not school_name or not teacher_name:

                    st.error(
                        "School name and teacher are required."
                    )

                else:

                    try:

                        # -------------------------------------------------
                        # Send ONE ROW PER DAY
                        # -------------------------------------------------
                        for day in range(1, num_days + 1):

                            row = {
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "School Name": school_name,
                                "Teacher Name": teacher_name,
                                "Number of Students": num_students,
                                "Travel Rep": travel_rep,
                                "Day": f"Day {day}",
                                "Enthusiasm": st.session_state.get(
                                    f"enthusiasm_{school_index}_{day}",
                                    ""
                                ),
                                "Comments": st.session_state.get(
                                    f"comments_{school_index}_{day}",
                                    ""
                                ),
                                "Notes": st.session_state.get(
                                    f"notes_{school_index}_{day}",
                                    ""
                                ),
                                "Photos": ""
                            }

                            response = requests.post(
                                WEBHOOK_URL,
                                json=row
                            )

                        # -------------------------------------------------
                        # Success
                        # -------------------------------------------------
                        if response.status_code == 200:

                            st.session_state[submitted_key] = True
                            st.session_state[submit_key] = False
                            st.session_state[confirm_key] = False

                            st.success(
                                f"🎉 School {school_index} submitted successfully!"
                            )

                        else:

                            st.error(
                                "❌ Failed to send data to Google Sheets."
                            )

                            st.write(
                                "Status code:",
                                response.status_code
                            )

                    except Exception as e:

                        st.error(
                            "❌ Connection error while sending data."
                        )

                        st.write(str(e))
