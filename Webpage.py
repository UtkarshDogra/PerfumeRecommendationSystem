import streamlit as st
import pandas as pd
from NLP_Code import recommendFragrance  # Import the function from the correct file

# Streamlit webpage
st.set_page_config(page_title="Fragrance Recommendation Chatbot", layout="wide")

# CSS for custom styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f9f9f9;
    }
    .title {
        text-align: center;
        color: #4CAF50;
        font-size: 2.5em;
        margin: 20px 0;
    }
    .input-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .input-container input {
        padding: 10px;
        border: 2px solid #4CAF50;
        border-radius: 5px;
        width: 50%;
        font-size: 1em;
    }
    .input-container button {
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1em;
        margin-left: 10px;
    }
    .input-container button:hover {
        background-color: #45a049;
    }
    .table-container {
        margin-top: 20px;
        overflow-x: auto;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        background-color: white;
    }
    th {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
    }
    td {
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }
    tr:hover {
        background-color: #f1f1f1;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title
st.markdown("<h1 class='title'>Fragrance Recommendation Chatbot</h1>", unsafe_allow_html=True)

# User input
user_input = st.text_input("Enter your fragrance preferences:", "")

# Button to process the input
if st.button("Run Chatbot"):
    if user_input:
        # Call the recommendFragrance function from NLP Code.py
        st.session_state.results = recommendFragrance(user_input)  # The function returns a list of dictionaries
    else:
        st.warning("Please enter a message before submitting!")

# If results are present, display them in a table
if 'results' in st.session_state and st.session_state.results:
    st.write("Recommended Fragrances:")
    
    # Convert the list of dictionaries to a DataFrame, explicitly defining columns
    df = pd.DataFrame(st.session_state.results, columns=["Brand", "Name", "Notes", "Description", "See Image"])
    
    # Add a Rank column starting from 1
    df.reset_index(drop=True, inplace=True)  # Reset index to start from 0
    df['Recommendation Rank'] = df.index + 1  # Create a new Rank column starting from 1
    
    # Reorder columns to place 'Rank' at the front
    df = df[['Recommendation Rank', 'Brand', 'Name', 'Notes', 'Description', 'See Image']]
    
    # Function to create clickable links for 'See Image'
    def make_clickable(link):
        return f'<a href="{link}" target="_blank">See Image</a>' if link else "No Image"

    # Apply make_clickable function to the 'See Image' column to create hyperlinks
    df['See Image'] = df['See Image'].apply(make_clickable)
    
    # Display the table with HTML rendering for hyperlinks
    st.markdown('<div class="table-container">' + df.to_html(escape=False, index=False) + '</div>', unsafe_allow_html=True)

# Reset button to clear the results
if st.button("Reset"):
    st.session_state.results = None
    st.experimental_rerun()  # Rerun the app to reset the state
