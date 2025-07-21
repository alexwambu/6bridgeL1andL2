import os
import streamlit as st

# === Embedded requirements.txt ===
requirements = """
streamlit==1.35.0
web3==6.15.1
"""

# === Embedded .streamlit/config.toml ===
config_toml = """
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection=false
"""

# Write embedded deployment files
if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")

with open("requirements.txt", "w") as f:
    f.write(requirements.strip())

with open(".streamlit/config.toml", "w") as f:
    f.write(config_toml.strip())

st.success("✅ Deployment files written")

# Optional: auto-load app.py
st.markdown("Run your app with:")
st.code("streamlit run app.py", language="bash")
