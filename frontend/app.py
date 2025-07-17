import streamlit as st
import requests

st.title("GitHub Issue Analyzer")

repo_url = st.text_input("GitHub Repository URL", "https://github.com/facebook/react")
issue_number = st.number_input("Issue Number", min_value=1, step=1)

if st.button("Analyze Issue"):
    if not repo_url or not issue_number:
        st.error("Please provide both a repository URL and an issue number.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze_issue",
                    json={"repo_url": repo_url, "issue_number": int(issue_number)}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis Complete!")
                    st.json(result)
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}") 