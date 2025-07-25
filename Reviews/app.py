import streamlit as st
from analyze_reviews import analyze

st.set_page_config(page_title="AI Review Analyzer", page_icon="🔍")
st.title("🔍 AI Customer Review Analyzer")

# Collect store name and location separately
store_name = st.text_input("Enter store name", placeholder="E.g., Cafe Rio")
location = st.text_input("Enter location", placeholder="E.g., Chicago")

if st.button("Analyze") and store_name.strip() and location.strip():
    query_params = {"store_name": store_name.strip(), "location": location.strip()}
    with st.spinner("Fetching reviews…"):
        result = analyze(query_params)
    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader("Summary")
        st.write(result["summary"])
        with st.expander("Sample reviews"):
            for r in result["samples"]:
                st.markdown(f"- {r}")
else:
    st.info("Please enter both store name and location to analyze reviews.")
