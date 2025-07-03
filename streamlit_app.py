
import streamlit as st
import requests
import tempfile
import os

st.set_page_config(page_title="Wapiti Web Vulnerability Scanner", layout="wide")

st.title("🛡️ Wapiti Web Vulnerability Scanner (Streamlit Community Edition)")

target_url = st.text_input("🔗 Enter Target URL", placeholder="https://example.com")

run_scan = st.button("🚀 Run Scan")

if run_scan and target_url:
    with st.spinner("Running scan... Please wait."):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.html")
            try:
                import wapitiCore.wapiti as wapiti
            except ImportError:
                st.error("Wapiti module not available. Streamlit Cloud does not support it directly.")
                st.info("Please run this app locally with `pip install wapiti3`.")
            else:
                try:
                    scanner = wapiti.Wapiti()
                    scanner.scan(target_url, scope="folder")
                    scanner.report(report_type="html", output_file=output_path)
                    st.success("Scan completed!")
                    with open(output_path, "r", encoding="utf-8", errors="ignore") as f:
                        html_report = f.read()
                    st.components.v1.html(html_report, height=600, scrolling=True)
                except Exception as e:
                    st.error(f"Scan failed: {e}")
else:
    st.info("Enter a valid target URL and click 'Run Scan'.")
