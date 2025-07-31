import streamlit as st
from datetime import datetime, timedelta

# Informasi ruangan
room_profiles = {
    "VIP Room 1": {
        "image": "images/vip1.jpg",
        "desc": "Private room with leather chairs, projector, and AC.",
        "facilities": ["✅ AC", "✅ Projector", "✅ Mini Bar", "✅ VIP Sofa"]
    },
    "VIP Room 2": {
        "image": "images/vip2.jpg",
        "desc": "Modern VIP room with soundproofing and lounge area.",
        "facilities": ["✅ AC", "✅ Whiteboard", "✅ Soundproof", "✅ Coffee Machine"]
    },
    "Meeting Room 1": {
        "image": "images/meeting1.jpg",
        "desc": "Standard meeting room for 10-12 people.",
        "facilities": ["✅ AC", "✅ Projector", "✅ Whiteboard"]
    },
    "Meeting Room 2": {
        "image": "images/meeting2.jpg",
        "desc": "Cozy meeting room with city view.",
        "facilities": ["✅ AC", "✅ TV Display", "✅ Flipchart"]
    },
    "Meeting Room 3": {
        "image": "images/meeting3.jpg",
        "desc": "Spacious room, suitable for workshops.",
        "facilities": ["✅ AC", "✅ Whiteboard", "✅ Projector"]
    },
    "Main Meeting Room": {
        "image": "images/main.jpg",
        "desc": "Main hall for large meetings up to 30 people.",
        "facilities": ["✅ AC", "✅ Projector", "✅ Microphone", "✅ Podium"]
    }
}

# Daftar ruangan meeting
room_list = list(room_profiles.keys())

# Inisialisasi session state
if "bookings" not in st.session_state:
    st.session_state.bookings = []

# Title dan Intro
st.title("📅 Meeting Room Booking System")
st.caption("Book a room and avoid scheduling conflicts. Built with 💙 Streamlit.")

# --------------------
# ROOM PROFILE SECTION
# --------------------
st.header("🏢 Meeting Room Profiles")
with st.expander("📖 View Room Details"):
    for room in room_list:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(room_profiles[room]["image"], width=200, caption=room)
        with col2:
            st.subheader(room)
            st.write(room_profiles[room]["desc"])
            st.markdown("**Facilities:**")
            st.markdown("\n".join(room_profiles[room]["facilities"]))
        st.markdown("---")

# ----------------
# BOOKING SECTION
# ----------------
st.header("📝 Book a Meeting Room")

with st.form("booking_form"):
    name = st.text_input("👤 Your Name")
    room = st.selectbox("🏛 Select Room", room_list)
    purpose = st.text_input("✍️ Purpose of Meeting")
    date_selected = st.date_input("📅 Meeting Date", datetime.today())
    start_time = st.time_input("⏰ Start Time", datetime.now().time())
    end_time = st.time_input("🔚 End Time", (datetime.now() + timedelta(hours=1)).time())
    submitted = st.form_submit_button("✅ Book Room")

    if submitted:
        start_dt = datetime.combine(date_selected, start_time)
        end_dt = datetime.combine(date_selected, end_time)

        if name.strip() == "" or purpose.strip() == "":
            st.warning("Please fill in all fields.")
        elif end_dt <= start_dt:
            st.error("End time must be after start time.")
        else:
            # Cek konflik
            conflict = False
            for booking in st.session_state.bookings:
                if booking['room'] == room:
                    existing_start = booking['start']
                    existing_end = booking['end']
                    if (start_dt < existing_end and end_dt > existing_start):
                        conflict = True
                        break

            if conflict:
                st.error(f"❌ {room} is already booked during that time.")
            else:
                st.session_state.bookings.append({
                    "name": name,
                    "room": room,
                    "purpose": purpose,
                    "start": start_dt,
                    "end": end_dt
                })
                st.success(f"✅ Room {room} booked for {name} on {date_selected.strftime('%Y-%m-%d')}.")

# ----------------------
# BOOKING SCHEDULE VIEW
# ----------------------
st.header("📋 Booking Schedule")
selected_date = st.date_input("📆 Filter by Date", datetime.today(), key="filter_date")

filtered_bookings = [b for b in st.session_state.bookings if b['start'].date() == selected_date]

if not filtered_bookings:
    st.info("No bookings on this date.")
else:
    for booking in sorted(filtered_bookings, key=lambda x: x['start']):
        with st.container():
            st.markdown(f"""
            ### 🏢 {booking['room']}
            - 👤 **Name:** {booking['name']}
            - ✍️ **Purpose:** {booking['purpose']}
            - 🕒 **Time:** {booking['start'].strftime("%H:%M")} - {booking['end'].strftime("%H:%M")}
            """)
            st.markdown("---")

# Developer tool (opsional)
with st.expander("🛠 Developer Options"):
    if st.button("🗑 Clear All Bookings"):
        st.session_state.bookings.clear()
        st.success("All bookings cleared.")
