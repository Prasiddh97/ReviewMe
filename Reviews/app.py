import streamlit as st
from analyze_reviews import analyze

st.set_page_config(page_title="AI Review Analyzer", page_icon="🔍")
st.title("🔍 AI Customer Review Analyzer")

# Removed microphone input option for now; only keep manual text input
q = st.text_input("Enter query (e.g., yelp:4kMBvIEWPxWkWKFN__8SxQ or https://example.com)")

if st.button("Analyze") and q:
    with st.spinner("Fetching reviews…"):
        result = analyze(q.strip())
    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader("Summary")
        st.write(result["summary"])
        with st.expander("Sample reviews"):
            for r in result["samples"]:
                st.markdown(f"- {r}")
