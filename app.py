import streamlit as st
import pandas as pd
import base64
import random

# Load CSV file
def load_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

# Get a random row without a user decision
def get_random_row(df):
    available_rows = df[df['user decision'] == ""].index.tolist()
    if not available_rows:
        return None
    return random.choice(available_rows)

# Count the number of unassigned rows
def count_unassigned_rows(df):
    return len(df[df['user decision'] == ""])

# Main app
def main():
    st.title("CSV Viewer and Editor")

    # Upload CSV
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        if 'data' not in st.session_state:
            st.session_state.data = load_csv(uploaded_file)

        if st.session_state.data is not None:
            df = st.session_state.data

            # Add 'user decision' column if not present
            if 'user decision' not in df.columns:
                df['user decision'] = ""

            # Session state for row index and history
            if 'row_index' not in st.session_state:
                st.session_state.row_index = get_random_row(df)
            if 'history' not in st.session_state:
                st.session_state.history = []

            # Display the number of unassigned rows
            st.write(f"Non-labeled number of rows: {count_unassigned_rows(df)}")

            # Display row
            if st.session_state.row_index is not None:
                row = df.loc[st.session_state.row_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2', 'user decision']]
                edited_row = st.experimental_data_editor(row, num_rows="fixed")

                # Update the user decision in the dataframe
                df.at[st.session_state.row_index, 'user decision'] = edited_row['user decision'].values[0]

                # Button logic
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Back"):
                        if st.session_state.history:
                            st.session_state.row_index = st.session_state.history.pop()
                with col2:
                    if st.button("Next"):
                        st.session_state.history.append(st.session_state.row_index)
                        st.session_state.row_index = get_random_row(df)

                # Download updated CSV
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                href = f'<a href="data:file/csv;base64,{b64}" download="updated.csv">Download Updated CSV</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

    