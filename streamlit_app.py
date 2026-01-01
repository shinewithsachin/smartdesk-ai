import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000"  
ADMIN_PASSWORD = "admin"

st.set_page_config(page_title="Ticket Intelligence System", page_icon="🎫", layout="wide")

if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False

st.title("🎫 SmartDesk AI")
st.markdown("### Intelligent IT Support & Ticket Automation System")
st.divider()

# --- SIDEBAR ---
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", ["Submit Ticket", "Track Ticket", "Admin Login"])

# --- PAGE 1: SUBMIT TICKET ---
if page == "Submit Ticket":
    st.header("📩 Submit a Support Ticket")
    with st.form("ticket_form"):
        subject = st.text_input("Subject")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Submit Ticket")

        if submitted and description:
            payload = {"subject": subject, "description": description}
            try:
                res = requests.post(f"{API_URL}/tickets/", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Ticket Submitted!")
                    
                    # FIX 1: Robust ID Handling (Handles 'id' or '_id')
                    ticket_id = data.get('id') or data.get('_id')
                    if ticket_id:
                        st.code(ticket_id, language="text")
                        st.info("⚠️ Copy the Ticket ID above to track your status later.")
                    else:
                        st.warning("Ticket submitted, but ID was missing in response.")
                else:
                    st.error(f"Failed to submit. Status: {res.status_code}")
            # FIX 2: Show the REAL error instead of generic "Connection Failed"
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- PAGE 2: TRACK TICKET (User View) ---
elif page == "Track Ticket":
    st.header("🔍 Track Your Ticket Status")
    ticket_id_input = st.text_input("Enter your Ticket ID:")
    
    if st.button("Check Status"):
        if ticket_id_input:
            try:
                res = requests.get(f"{API_URL}/tickets/") 
                tickets = res.json()
                my_ticket = next((t for t in tickets if t['id'] == ticket_id_input or t.get('_id') == ticket_id_input), None)
                
                if my_ticket:
                    st.divider()
                    st.subheader(f"Ticket: {my_ticket['subject']}")
                    
                    status = my_ticket.get('status', 'open')
                    if status == 'open':
                        st.warning(f"Status: {status.upper()}")
                    else:
                        st.success(f"Status: {status.upper()}")

                    st.markdown(f"**Description:** {my_ticket['description']}")
                    
                    # SHOW REPLY
                    solution = my_ticket.get('solution')
                    
                    # Debug helper (Optional: remove later)
                    if status == 'closed' and not solution:
                        st.warning("Debug: Ticket is closed but solution is empty.")

                    if solution:
                        st.info("✅ **Support Team Reply:**")
                        st.write(solution)
                    else:
                        st.info("⏳ Our team is working on your request.")
                else:
                    st.error("Ticket ID not found.")
            except Exception as e:
                st.error(f"Error: {e}")

# --- PAGE 3: ADMIN LOGIN ---
elif page == "Admin Login":
    # Login Logic
    if not st.session_state['is_admin']:
        pwd = st.sidebar.text_input("Admin Password", type="password")
        if st.sidebar.button("Login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state['is_admin'] = True
                st.rerun()
            else:
                st.sidebar.error("Wrong Password")
    
    # Admin Dashboard
    if st.session_state['is_admin']:
        st.header("📊 Admin Dashboard")
        if st.button("Logout"):
            st.session_state['is_admin'] = False
            st.rerun()
            
        try:
            res = requests.get(f"{API_URL}/tickets/")
            if res.status_code == 200:
                tickets = res.json()
                df = pd.DataFrame(tickets)
                
                # 1. METRICS
                c1, c2 = st.columns(2)
                c1.metric("Total Tickets", len(df))
                c2.metric("Open Tickets", len(df[df['status'] == 'open']))
                
                st.divider()

                # 2. CHARTS
                if not df.empty:
                    chart1, chart2 = st.columns(2)
                    with chart1:
                        st.subheader("Tickets by Category")
                        fig_cat = px.bar(df, x='category', color='category', title="Category Distribution")
                        st.plotly_chart(fig_cat, use_container_width=True)
                    
                    with chart2:
                        st.subheader("Tickets by Priority")
                        fig_pri = px.pie(df, names='priority', title="Priority Breakdown", hole=0.4)
                        st.plotly_chart(fig_pri, use_container_width=True)

                st.divider()
                
                # 3. TICKET MANAGEMENT
                st.subheader("🛠️ Resolve Tickets")
                
                open_tickets = [t for t in tickets if t.get('status') == 'open']
                
                if not open_tickets:
                    st.success("🎉 No open tickets! Good job.")
                else:
                    options = {f"{t.get('id', t.get('_id'))} - {t['subject']}": t.get('id', t.get('_id')) for t in open_tickets}
                    selected_label = st.selectbox("Select Ticket to Resolve:", list(options.keys()))
                    
                    if selected_label:
                        t_id = options[selected_label]
                        ticket = next(t for t in tickets if t.get('id', t.get('_id')) == t_id)
                        
                        st.write(f"**Issue:** {ticket['description']}")
                        st.write(f"**AI Priority:** `{ticket.get('priority')}`")
                        
                        # Generate Draft
                        if st.button("🤖 Generate Draft Reply"):
                            with st.spinner("Asking AI..."):
                                api_res = requests.post(f"{API_URL}/tickets/{t_id}/reply")
                                if api_res.status_code == 200:
                                    st.session_state['draft_reply'] = api_res.json()['ai_reply']
                                else:
                                    st.error("AI Failed.")
                        
                        # Edit & Send
                        draft = st.session_state.get('draft_reply', "")
                        final_response = st.text_area("Final Response to User:", value=draft, height=150)
                        
                        if st.button("🚀 Send Reply & Close Ticket"):
                            if final_response:
                                update_payload = {
                                    "status": "closed",
                                    "solution": final_response
                                }
                                # Call PATCH
                                patch_res = requests.patch(f"{API_URL}/tickets/{t_id}", json=update_payload)
                                
                                if patch_res.status_code == 200:
                                    st.success("Ticket Closed and Reply Sent!")
                                    if 'draft_reply' in st.session_state:
                                        del st.session_state['draft_reply']
                                    st.rerun()
                                else:
                                    st.error(f"Failed to update ticket. Status: {patch_res.status_code}")
                            else:
                                st.warning("⚠️ Reply cannot be empty.")
            else:
                st.error("Failed to fetch data from backend.")
        except Exception as e:
             st.error(f"Connection Error: {e}")