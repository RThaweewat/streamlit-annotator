import streamlit as st
import pandas as pd
import base64

st. set_page_config(layout="wide")

# Load CSV file
def load_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

# Get the next row without a user decision
def get_next_row(df, current_index):
    available_rows = df[df['user decision'] == ""].index.tolist()
    available_rows = [row for row in available_rows if row > current_index]
    if not available_rows:
        return None
    return min(available_rows)

# Main app
def main():
    if 'history' not in st.session_state:
    st.session_state.history = []
    st.title("CSV Annotator V1.0")

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

            # Initialize current index
            if 'current_index' not in st.session_state:
                st.session_state.current_index = df.index[0]

            # Display row
            if st.session_state.current_index is not None:
                row = df.loc[st.session_state.current_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2']]
                st.dataframe(row, width=1200)

                # Button logic
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("Unknown"):
                        if st.session_state.current_index is not None:
                            df.at[st.session_state.current_index, 'user decision'] = "unknown"
                            st.session_state.current_index = get_next_row(df, st.session_state.current_index)
                with col2:
                    if st.button("Next Match"):
                        if st.session_state.current_index is not None:
                            df.at[st.session_state.current_index, 'user decision'] = "match"
                            st.session_state.current_index = get_next_row(df, st.session_state.current_index)
                with col3:
                    if st.button("Next Non-Match"):
                        if st.session_state.current_index is not None:
                            df.at[st.session_state.current_index, 'user decision'] = "non match"
                            st.session_state.current_index = get_next_row(df, st.session_state.current_index)
                with col4:
                    if st.button("Back"):
                        if st.session_state.current_index != df.index[0]:
                            st.session_state.current_index -= 1
                            df.at[st.session_state.current_index, 'user decision'] = ""
                            try:
                                st.session_state.history.remove(st.session_state.current_index)
                            except ValueError:
                                pass

                # Download updated CSV
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                href = f'<a href="data:file/csv;base64,{b64}" download="updated.csv">Download Updated CSV</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

    
