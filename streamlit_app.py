import streamlit as st
import subprocess
import os
import tempfile
import shutil

st.set_page_config(page_title="Wapiti Web Scanner", layout="centered")

st.title("🔍 Wapiti Web Vulnerability Scanner")

target = st.text_input("Enter target URL (e.g. https://testphp.vulnweb.com):")

if st.button("Start Scan"):
    if not target.strip():
        st.warning("Please enter a valid target URL.")
    else:
        with st.spinner("Scanning... please wait."):
            # Create a temporary directory for the report
            temp_dir = tempfile.mkdtemp()
            try:
                command = [
                    "python", "-m", "wapiti",
                    "-u", target,
                    "-f", "html",
                    "-o", temp_dir,
                    "-v", "2"
                ]
                result = subprocess.run(command, capture_output=True, text=True)

                st.success("✅ Scan complete!")

                st.subheader("📜 Raw Wapiti Output")
                st.code(result.stdout if result.stdout else "[No output]")

                report_path = os.path.join(temp_dir, "index.html")
                if os.path.exists(report_path):
                    with open(report_path, "r", encoding="utf-8") as f:
                        report_data = f.read()
                    st.subheader("🧾 HTML Report Preview")
                    st.components.v1.html(report_data, height=500, scrolling=True)
                    st.download_button("⬇️ Download Report", data=report_data, file_name="wapiti_report.html", mime="text/html")
                else:
                    st.warning("No HTML report generated.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                shutil.rmtree(temp_dir)
