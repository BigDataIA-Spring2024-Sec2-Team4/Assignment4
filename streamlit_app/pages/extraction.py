import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Projects",
)

# Main page title
st.title("Projects")

# Sidebar message
st.sidebar.success("Select a page above.")

# Retrieve my_input from session state with default value
my_input = st.session_state.get("my_input", "")


# If user clicks on "Extract" button
if st.button("Extract"):
    # Code to trigger Airflow for data extraction
    st.write("Data extraction initiated!")

# If user clicks on "Display" button
if st.button("Display"):
    # Mocking data retrieval from Snowflake (replace with actual data retrieval code)
    data = {
        'Project Name': ['Project A', 'Project B', 'Project C'],
        'Start Date': ['2022-01-01', '2022-02-01', '2022-03-01'],
        'End Date': ['2022-06-30', '2022-07-31', '2022-08-31']
    }
    df = pd.DataFrame(data)
    
    # Display the DataFrame
    st.write("Displaying results...")
    st.write(df)
