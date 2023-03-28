import streamlit as st
import os
import psycopg2

# specify user/password/where the database is
host: str = os.environ.get("HOST")
sqluser: str = os.environ.get("SQLUSER")
sqlpass: str = os.environ.get("SQLPASS")
dbname: str = os.environ.get("DBNAME")

conn = psycopg2.connect(dbname=dbname, user=sqluser,
                        password=sqlpass, host=host)

cur = conn.cursor()


st.set_page_config(page_title="Admin")

st.title("Summary")

option = st.selectbox("Attendee Status", ("<Select>", "Not Checked In", "Checked In (In the event)", "Checked Out"))

if option == "Not Checked In":
    cur.execute("""select a.*, b.attendee_id 
    from "Attendee" a 
    left join "Attendee_inout" b on a.id = b.attendee_id 
    where b.check_type is null
    """)

    records = cur.fetchall()
    st.write(f"Number of people not checked in: {len(records)}")
    st.table(records)

elif option == "Checked In (In the event)":
    cur.execute("""select attendee_id, check_type from (select distinct on (attendee_id) *
    from "Attendee_inout"
    order by attendee_id, timestamp desc) as c
    where check_type = 'in'
    """)

    records = cur.fetchall()
    st.write(f"Number of people in the event: {len(records)}")
    st.table(records)

elif option == "Checked Out":
    cur.execute("""select attendee_id, check_type from (select distinct on (attendee_id) *
    from "Attendee_inout"
    order by attendee_id, timestamp desc) as c
    where check_type = 'out'
    """)

    records = cur.fetchall()
    st.write(f"Number of people checked out: {len(records)}")
    st.table(records)

