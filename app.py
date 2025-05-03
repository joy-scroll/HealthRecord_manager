import streamlit as st
import os
import sqlite3
import base64
from datetime import datetime
from utils.visualization import plot_metric_trend
from models.summarizer import summarize_report
from security.encryptor import encrypt_file, decrypt_file

DB_PATH = "records.db"
UPLOAD_DIR = "uploaded_records"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    category TEXT,
    upload_date TEXT,
    summary TEXT
)""")
conn.commit()

st.set_page_config(page_title="Personal Health Record Manager", layout="wide")
st.title("🏥 Personal Health Record Manager")

# Upload section
st.sidebar.header("📤 Upload Record")
file = st.sidebar.file_uploader("Upload PDF/Image", type=["pdf", "jpg", "png"])
category = st.sidebar.selectbox("Category", ["General", "Dental", "Lab Results", "Orthopedic", "Gynecological"])

if file:
    upload_date = datetime.now().isoformat()
    filepath = os.path.join(UPLOAD_DIR, file.name)
    with open(filepath, "wb") as f:
        f.write(file.read())
    
    summary = summarize_report(filepath)
    
    c.execute("INSERT INTO records (filename, category, upload_date, summary) VALUES (?, ?, ?, ?)",
              (file.name, category, upload_date, summary))
    conn.commit()
    st.sidebar.success("File uploaded and summarized!")

st.header("📁 Your Medical Records")
c.execute("SELECT id, filename, category, upload_date, summary FROM records ORDER BY upload_date DESC")
rows = c.fetchall()

for row in rows:
    st.subheader(f"📝 {row[1]} ({row[2]})")
    st.caption(f"Uploaded on {row[3]}")
    st.write(row[4])
    with st.expander("Show Visualization"):
        st.altair_chart(plot_metric_trend())
    st.markdown("---")
