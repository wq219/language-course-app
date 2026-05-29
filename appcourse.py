import streamlit as st
import mysql.connector
import pandas as pd

# --- KONFIGURASI DATABASE ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="WildanQonita21",
        database="course_registration"
    )

# --- SETTING DESAIN & PAGE AESTHETIC ---
st.set_page_config(page_title="LinguaConnect Portal", layout="centered")

# Custom CSS untuk implementasi warna Sage Green & Soft Pink serta Font Modern
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .main, .stApp { 
        background-color: #F9F9F8 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Typography */
    h1 { 
        color: #4A5243 !important; 
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    h2, h3, p, label, .stMarkdown { 
        color: #5A6353 !important; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Info/Course Cards - Sage Green Accent */
    .stAlert {
        background-color: #CFD5C7 !important;
        color: #4A5243 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-weight: 500;
    }
    .stAlert p { color: #4A5243 !important; }

    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px !important;
        border: 1px solid #E2E4E0 !important;
        background-color: #FFFFFF !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #FCDEEA !important;
        box-shadow: 0 0 0 2px #FCDEEA !important;
    }

    /* Primary Buttons - Soft Pink Accent */
    .stButton>button { 
        background-color: #FCDEEA !important; 
        color: #5A3E4B !important; 
        border: 1px solid #F7C6DC !important;
        border-radius: 8px !important; 
        width: 100%;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #F7C6DC !important; 
        color: #5A3E4B !important;
        border-color: #F7C6DC !important;
        transform: translateY(-1px);
    }
    
    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #EAECE7 !important;
    }
    [data-testid="stSidebar"] .stRadio>label {
        color: #4A5243 !important;
        font-weight: 500;
    }
    
    /* Divider */
    hr { border-top: 1px solid #E2E4E0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- IDENTITAS ADMIN (HARDCODED) ---
ADMIN_USER = "ADMINCODING8XX12"
ADMIN_PASS = "8EIGHTFOUR4CODING"

# --- HEADER APLIKASI ---
st.title("LinguaConnect")
st.write("Language Course Registration System")
st.write("---")

# --- NAVIGASI SIDEBAR ---
st.sidebar.markdown("<p style='font-weight:600; color:#4A5243; margin-bottom:5px;'>Navigation</p>", unsafe_allow_html=True)
role = st.sidebar.radio("Select your role:", ["Student Registration", "Admin Portal"], label_visibility="collapsed")

# --- MODUL 1: STUDENT FLOW ---
if role == "Student Registration":
    st.subheader("Student Registration Form")
    st.write("Please fill in your details to enroll in our language programs.")
    
    courses = ["English Intensive", "Conversational Japanese", "Business German", "Mandarin Beginner", "K-Pop Korean Level 1"]
    
    st.write("### Available Courses")
    cols = st.columns(3)
    for i, c in enumerate(courses):
        cols[i % 3].info(c)
        
    st.write("---")
    
    with st.form(key="reg_form", clear_on_submit=True):
        student_name = st.text_input("Full Name", placeholder="e.g. John Doe")
        email = st.text_input("Email Address", placeholder="e.g. john@example.com")
        selected_course = st.selectbox("Choose Course", courses)
        submit_btn = st.form_submit_button(label="Submit Registration")
        
    if submit_btn:
        if student_name and email:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                query = "INSERT INTO registrations (student_name, email, course_name) VALUES (%s, %s, %s)"
                cursor.execute(query, (student_name, email, selected_course))
                conn.commit()
                cursor.close()
                conn.close()
                
                st.success(f"Registration successful. Welcome to {selected_course}, {student_name}.")
            except Exception as e:
                st.error(f"Database Error: {e}")
        else:
            st.warning("Please fill out all fields before submitting.")

# --- MODUL 2: ADMIN FLOW ---
elif role == "Admin Portal":
    st.subheader("Admin Authentication")
    st.write("Secure access for authorized administrators only.")
    
    input_user = st.text_input("Username", placeholder="Enter admin username")
    input_pass = st.text_input("Password", type="password", placeholder="Enter admin password")
    login_btn = st.button("Login")
    
    if login_btn:
        if input_user == ADMIN_USER and input_pass == ADMIN_PASS:
            st.session_state['admin_logged_in'] = True
        else:
            st.session_state['admin_logged_in'] = False
            st.error("Invalid Username or Password. Access Denied.")

    if st.session_state.get('admin_logged_in', False):
        st.write("---")
        st.subheader("Registered Students Report")
        
        try:
            conn = get_db_connection()
            query = "SELECT id, student_name AS 'Student Name', email AS 'Email', course_name AS 'Course', registration_date AS 'Date Registered' FROM registrations"
            df = pd.read_sql(query, conn)
            conn.close()
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.write("")
                st.download_button(
                    label="Export Report to CSV",
                    data=csv,
                    file_name='language_course_report.csv',
                    mime='text/csv',
                )
            else:
                st.info("No students have registered yet.")
                
        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
            
        st.write("")
        if st.button("Log Out"):
            st.session_state['admin_logged_in'] = False
            st.rerun() 