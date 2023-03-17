import streamlit as st
import pandas as pd

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")


@st.cache
def convert_df(dataframe: pd.DataFrame):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return dataframe.to_csv().encode('utf-8')


def display_row(session_state):
    if session_state.row_num < 0:
        session_state.row_num = 0
    elif session_state.row_num >= len(df):
        session_state.row_num = len(df) - 1

    row_to_display = df.iloc[session_state.row_num].to_frame().T
    edited_row = st.experimental_data_editor(row_to_display)

    return edited_row


uploaded_file = st.file_uploader("Choose your CSV file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

df['User Decision'] = ""
df['Row Number'] = range(len(df))

session_state = SessionState.get(row_num=0)

edited_row = display_row(session_state)

next_match = st.button("Next (Matched)")
next_not_match = st.button("Next (Not Matched)")
back = st.button("Back")

if next_match:
    df.loc[session_state.row_num, "User Decision"] = "Match"
    session_state.row_num += 1
    display_row(session_state)

elif next_not_match:
    df.loc[session_state.row_num, "User Decision"] = "Unmatch"
    session_state.row_num += 1
    display_row(session_state)

elif back:
    session_state.row_num -= 1
    display_row(session_state)

final_df = convert_df(df)
if final_df is not None:
    st.markdown("You can download edited file from download button below (CSV)")
    st.download_button(
        label="Download edited data as CSV",
        data=final_df,
        file_name='edited_data.csv',
        mime='text/csv',
    )
    