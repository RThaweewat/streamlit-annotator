import streamlit as st
import pandas as pd

# Define a function to load the CSV file
def load_csv(file):
    df = pd.read_csv(file)
    return df

# Define a function to display the current row
def display_row(df, row_idx):
    row = df.iloc[row_idx]
    st.write(row)

# Define the Streamlit app
def main():
    st.title("CSV Viewer")

    # Upload the CSV file
    file = st.file_uploader("Upload CSV file", type=["csv"])
    if file:
        # Load the CSV file
        df = load_csv(file)

        # Initialize the row index
        row_idx = 0

        # Display the current row
        display_row(df, row_idx)

        # Define the buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Match"):
                df.loc[row_idx, "user decision"] = "match"
                row_idx += 1
                display_row(df, row_idx)
        with col2:
            if st.button("Non Match"):
                df.loc[row_idx, "user decision"] = "non match"
                row_idx += 1
                display_row(df, row_idx)
        with col3:
            if st.button("Back"):
                if row_idx > 0:
                    row_idx -= 1
                    display_row(df, row_idx)
                else:
                    st.warning("You are at the beginning of the file.")

# Run the Streamlit app
if __name__ == "__main__":
    main()




