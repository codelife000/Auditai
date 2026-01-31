import streamlit as st
from scanner import scan_website
from ai_analyzer import analyze_with_ai
from utils import normalize_url, is_valid_url
from scoring import calculate_score
from dashboard import show_dashboard

st.set_page_config(page_title="AI Website Auditor", layout="wide")
st.title("🧠 AI Website Auditor - Advanced Hackathon Edition")
st.write("Paste a website URL and get a professional AI-powered audit with full visual stats.")

url = st.text_input("Enter Website URL")

if st.button("Scan Website"):
    if not url or not is_valid_url(url):
        st.warning("Please enter a valid URL")
    else:
        url = normalize_url(url)
        with st.spinner("Scanning website..."):
            scan_data = scan_website(url)

        if "error" in scan_data:
            st.error(scan_data["error"])
        else:
            # AI Analysis
            with st.spinner("Analyzing with AI..."):
                ai_report = analyze_with_ai(scan_data)

            # Dynamic scoring
            overall_score = calculate_score(scan_data)
            scan_data["overall_score"] = overall_score
            # Extra heuristic scores
            scan_data["seo_score"] = max(0, 100 - scan_data.get("images_without_alt",0)*5)
            scan_data["performance_score"] = max(0, 100 - scan_data.get("load_time",5)*10)
            scan_data["accessibility_score"] = max(0, 100 - scan_data.get("images_without_alt",0)*5)
            scan_data["security_score"] = 100 if scan_data.get("https") else 50

            # Show advanced dashboard
            show_dashboard(scan_data, ai_report)
