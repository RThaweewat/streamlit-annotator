import streamlit as st
import pandas as pd
import base64

st. set_page_config(layout="wide")

# Load CSV file
def load_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        df = df[df['HOUSE_FULL_1'].notna()]
        df = df[df['HOUSE_FULL_2'].notna()]
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
                
            # Display counters
            annotated_rows = df[df['user decision'] != ""].shape[0]
            left_rows = df[df['user decision'] == ""].shape[0]
            st.write(f"Annotated rows: {annotated_rows}")
            st.write(f"Left rows: {left_rows}")

            # Display row placeholder
            row_placeholder = st.empty()
            # Button logic
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                if st.button("Unknown"):
                    if st.session_state.current_index is not None:
                        st.session_state.history.append(st.session_state.current_index)
                        df.at[st.session_state.current_index, 'user decision'] = "unknown"
                        st.session_state.current_index = get_next_row(df, st.session_state.current_index)
                        row = df.loc[st.session_state.current_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2']]
                        row_placeholder.dataframe(row, width=1600)
                    else:
                        row_placeholder.warning("No more rows available.")
            with col3:
                if st.button("Next Match"):
                    if st.session_state.current_index is not None:
                        st.session_state.history.append(st.session_state.current_index)
                        df.at[st.session_state.current_index, 'user decision'] = "match"
                        st.session_state.current_index = get_next_row(df, st.session_state.current_index)
                        row = df.loc[st.session_state.current_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2']]
                        row_placeholder.dataframe(row, width=1600)
                    else:
                        row_placeholder.warning("No more rows available.")
            with col4:
                if st.button("Next Non-Match"):
                    if st.session_state.current_index is not None:
                        st.session_state.history.append(st.session_state.current_index)
                        df.at[st.session_state.current_index, 'user decision'] = "non match"
                        st.session_state.current_index = get_next_row(df, st.session_state.current_index)
                        row = df.loc[st.session_state.current_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2']]
                        row_placeholder.dataframe(row, width=1600)
                    else:
                        row_placeholder.warning("No more rows available.")
            with col5:
                if st.button("Back"):
                    if st.session_state.history:
                        st.session_state.current_index = st.session_state.history.pop()
                        df.at[st.session_state.current_index, 'user decision'] = ""
                        row = df.loc[st.session_state.current_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2']]
                        row_placeholder.dataframe(row, width=1600)
                    elif st.session_state.current_index != df.index[0]:
                        st.session_state.current_index -= 1
                        df.at[st.session_state.current_index, 'user decision'] = ""
                        row = df.loc[st.session_state.current_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2']]
                        row_placeholder.dataframe(row, width=1600)
                    else:
                        row_placeholder.warning("No more rows available.")
            with col2:
                if st.button("Not Address"):
                    if st.session_state.current_index is not None:
                        st.session_state.history.append(st.session_state.current_index)
                        df.at[st.session_state.current_index, 'user decision'] = "non address"
                        st.session_state.current_index = get_next_row(df, st.session_state.current_index)
                        row = df.loc[st.session_state.current_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2']]
                        row_placeholder.dataframe(row, width=1600)
                    else:
                        row_placeholder.warning("No more rows available.")

            if st.session_state.current_index is not None and (st.session_state.current_index - 1) not in st.session_state.history:
                st.session_state.history.append(st.session_state.current_index - 1)

            # Display row initially
            if st.session_state.current_index is None and not df[df['user decision'] == ""].empty:
                st.session_state.current_index = df[df['user decision'] == ""].index[0]

            if st.session_state.current_index is not None:
                try:
                    row = df.loc[st.session_state.current_index, ['HOUSE_FULL_1', 'HOUSE_FULL_2']]
                    row_placeholder.dataframe(row, width=1600)

                    user_decision = st.selectbox("Choose the correct option", ("", "HOUSE_FULL_1", "HOUSE_FULL_2"))

                    if user_decision:
                        df.loc[st.session_state.current_index, 'user decision'] = user_decision
                        st.session_state.current_index = None
                        st.success("Decision saved. Loading next row...")
                except KeyError:
                    st.session_state.current_index = None
                    row_placeholder.empty()
                    st.info("Thanks, all rows are filled.")
            else:
                row_placeholder.empty()
                st.info("Thanks, all rows are filled.")






            annotated_rowss = df[df['user decision'] != ""].shape[0]
            left_rowss = df[df['user decision'] == ""].shape[0]
            st.write(f"Annotated rows: {annotated_rowss}")
            st.write(f"Left rows: {left_rowss}")
            # Download updated CSV
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}" download="updated.csv">Download Updated CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

            st.dataframe(df[['HOUSE_FULL_1', 'HOUSE_FULL_2', 'user decision']], width=1600)



if __name__ == "__main__":
    main()

    
