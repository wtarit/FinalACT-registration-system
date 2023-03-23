import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import pytz

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
    student_id = st.text_input("Enter Student ID")
    if st.form_submit_button("Submit"):
        st.session_state["submit_button"] = True


# if the button is clicked, show student data
if st.session_state["submit_button"]:
    r = supabase.table("Attendee").select(
        '*').eq("id", int(student_id)).execute()
    if r.data == []:
        st.header(":red[No data found.]")
        st.session_state["submit_button"] = False
    else:
        data = r.data[0]
        # show attendee information
        st.write(f"Name: {data['Name']}")
        st.write(f"Tel: {data['Phone']}")
        st.image(
            f"{url}/storage/v1/object/public/attendee-image/{student_id}.webp")

        # Show attendance information
        r = supabase.table("Attendee_inout").select(
            "*").eq("attendee_id", int(student_id)).execute()
        data = r.data
        for row in data:
            utc = pytz.utc
            t = utc.localize(datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%S.%f"))
            bangkok = pytz.timezone("Asia/Bangkok")
            st.write(f"Check {row['check_type']} Time: {t.astimezone(bangkok).strftime('%H:%M')}")
        
        if data == [] or data[-1]["check_type"] == "out":
            if st.button("Check In"):
                supabase.table("Attendee_inout").insert(
                    {"attendee_id": student_id, "check_type": "in"}).execute()
                st.session_state["submit_button"] = False
                st.experimental_rerun()
        else:
            if st.button("Check Out"):
                supabase.table("Attendee_inout").insert(
                    {"attendee_id": student_id, "check_type": "out"}).execute()
                st.session_state["submit_button"] = False
                st.experimental_rerun()
