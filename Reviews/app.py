# app.py
import streamlit as st
from analyze_reviews import analyze
from review_fetcher import get_yelp_suggestions

st.set_page_config(page_title="AI Review Analyzer", page_icon="🔍")
st.title("🔍 AI Customer Review Analyzer")

# --- UI for finding and selecting a business ---
st.header("1. Find a Business")
search_term = st.text_input("Enter a store name", placeholder="E.g., dominos pizza")
location = st.text_input("Enter the location", placeholder="E.g., Ahmedabad")

# For now, suggestions are powered by Yelp, but the final analysis can use either source.
if st.button("Find Suggestions"):
    # (Suggestion logic remains the same)
    pass 

# ... (The rest of the suggestion selection UI remains the same)

# --- UI for analyzing the selected business ---
st.header("2. Analyze Reviews")

# Check if a business has been selected
if st.session_state.get('selected_store') and st.session_state.selected_store != "-- Select a Business --":
    selected_store = st.session_state.selected_store
    
    st.write(f"Ready to analyze: **{selected_store}** in **{location}**")

    # --- New dropdown to select the source ---
    source = st.selectbox("Select Review Source:", ["Yelp", "Google"])
    
    if st.button("Analyze Reviews"):
        query_params = {
            "source": source.lower(), # Pass the selected source
            "store_name": selected_store,
            "location": location
        }
        try:
            with st.spinner(f"Fetching {source} reviews and analyzing…"):
                result = analyze(query_params)
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.subheader("Summary")
                st.write(result["summary"])
                with st.expander("Sample Reviews"):
                    for r in result["samples"]:
                        st.markdown(f"- {r}")
        except Exception as e:
            st.error("An unexpected error occurred. Please try again later.")
            print(f"Error: {e}")
else:
    st.info("First, find and select a business to enable analysis.")
