import streamlit as st
from datetime import datetime, timedelta

# Daftar ruangan meeting
room_list = ["VIP Room 1", "VIP Room 2", "Meeting Room 1", "Meeting Room 2", "Meeting Room 3", "Main Meeting Room"]

# Inisialisasi session state
if "bookings" not in st.session_state:
    st.session_state.bookings = []

# Header
st.title("📅 Meeting Room Booking System")

# Form Booking
with st.form("booking_form"):
    st.subheader("🔒 Book a Room")
    name = st.text_input("Your Name")
    room = st.selectbox("Select Room", room_list)
    purpose = st.text_input("Purpose of Meeting")
    date_selected = st.date_input("Meeting Date", datetime.today())
    start_time = st.time_input("Start Time", datetime.now().time())
    end_time = st.time_input("End Time", (datetime.now() + timedelta(hours=1)).time())

    submitted = st.form_submit_button("Book Room")

    if submitted:
        start_dt = datetime.combine(date_selected, start_time)
        end_dt = datetime.combine(date_selected, end_time)

        if name.strip() == "" or purpose.strip() == "":
            st.warning("Please fill in all fields.")
        elif end_dt <= start_dt:
            st.error("End time must be after start time.")
        else:
            # Cek apakah ruangan tersedia
            conflict = False
            for booking in st.session_state.bookings:
                if booking['room'] == room:
                    existing_start = booking['start']
                    existing_end = booking['end']
                    # Cek overlap
                    if (start_dt < existing_end and end_dt > existing_start):
                        conflict = True
                        break

            if conflict:
                st.error(f"❌ {room} is already booked during that time.")
            else:
                # Simpan booking
                st.session_state.bookings.append({
                    "name": name,
                    "room": room,
                    "purpose": purpose,
                    "start": start_dt,
                    "end": end_dt
                })
                st.success(f"✅ Room {room} booked successfully for {name} on {date_selected}!")

# Tampilkan semua booking
st.subheader("📋 Booking Schedule")
selected_date = st.date_input("Filter by Date", datetime.today())

filtered_bookings = [b for b in st.session_state.bookings if b['start'].date() == selected_date]
if not filtered_bookings:
    st.info("No bookings on this date.")
else:
    for booking in sorted(filtered_bookings, key=lambda x: x['start']):
        st.markdown(f"""
        ### 🏢 {booking['room']}
        - **Name:** {booking['name']}
        - **Purpose:** {booking['purpose']}
        - **Time:** {booking['start'].strftime("%H:%M")} - {booking['end'].strftime("%H:%M")}
        """)

# Tombol reset (opsional)
if st.button("🗑 Clear All Bookings (dev only)"):
    st.session_state.bookings.clear()
    st.success("All bookings cleared.")
