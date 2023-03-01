import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


st.set_page_config(page_title="Final ACT Registration")

# create a title for the app
st.title("Final ACT Registration")

if "submit_button" not in st.session_state:
    st.session_state["submit_button"] = False

with st.form(key="Attendee Details", clear_on_submit=True):
    # create a textbox to receive student id
    student_id = st.text_input("Enter Student ID", )
    if st.form_submit_button("Submit"):
        st.session_state["submit_button"] = not st.session_state["submit_button"]


# if the button is clicked, show student data
if st.session_state["submit_button"]:
    r = supabase.table('Attendee').select(
        '*').eq("id", int(student_id)).execute()
    data = r.data
    st.write(data[0]["Name"])
    # show image
    st.image(
        f"{url}/storage/v1/object/public/attendee-image/{student_id}.webp")
    st.write(data[0]["email"])
    # create radio buttons to select the attendance check in / check out
    attendance = st.radio("Attendance", ("Check In", "Check Out"))
    # create a button to submit the attendance
    submit_attendance = st.button("Submit Attendance")

    # if the button is clicked, show the attendance
    if submit_attendance:
        print(attendance)
        st.session_state["submit_button"] = False
        st.experimental_rerun()
