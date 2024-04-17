import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Monthly Student Monitoring")
st.markdown("Enter the details of the students below.")

# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing data
existing_data = conn.read(worksheet="Data", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")

GRADES = [
    "K1",
    "K2",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
    "G7",
    "G8"
]

MONTHS = [
    "Baishak",
    "Jestha",
    "Ashad",
    "Shrawn",
    "Bhadra",
    "Ashoj",
    "Kartik",
    "Mangsir",
    "Poush",
    "Magh",
    "Falgun",
    "Chaitra"
]

# Onboarding New Vendor Form
with st.form(key="student_form"):
    school_name = st.text_input(label="School Name")
    grade = st.selectbox("Grade", options=GRADES, index=None)
    months = st.selectbox("Monitoring Month", options=MONTHS, index=None)
    total_students = st.text_input(label="Total Number of Students")
    total_males = st.text_input(label="Total Male Students")
    total_females = st.text_input(label="Total Female Students")
    opening_days = st.text_input(label="Total Opening Days in Month")

    submit_button = st.form_submit_button(label="Submit Details")



    if submit_button:
        # Check if all mandatory fields are filled
        if not school_name or not grade:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        else:
            # Create a new row of student data
            student_data = pd.DataFrame(
                [
                    {
                        "School Name" : school_name,
                        "Grade" : grade,
                        "Month" :  months, 
                        "Total Students" : total_students,
                        "Total Males" : total_males,
                        "Total Females" : total_females,
                        "Opening Days" : opening_days,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, student_data], ignore_index=True)

            # Update Google Sheets with the new student data
            conn.update(worksheet="Data", data=updated_df)

            st.success("Details successfully submitted")
   

st.dataframe(existing_data)

sql='''
SELECT
    "School Name",
    "Grade",
    "Monitoring Month",
    "Total Students",
    "Total Males",
    "Total Females",
    "Opening Days"
FROM
    Data
'''




   