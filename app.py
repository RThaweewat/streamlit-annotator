import streamlit as st
import pandas as pd

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")


@st.cache
def convert_df(dataframe: pd.DataFrame):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return dataframe.to_csv().encode('utf-8')


def display_row():
    row_num = st.session_state.row_num
    if row_num < 0:
        row_num = 0
    elif row_num >= len(df):
        row_num = len(df) - 1

    row_to_display = df.iloc[row_num].to_frame().T
    edited_row = st.experimental_data_editor(row_to_display)
    return edited_row


uploaded_file = st.file_uploader("Choose your CSV file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

df['User Decision'] = ""
df['Row Number'] = range(len(df))

if 'row_num' not in st.session_state:
    st.session_state.row_num = 0

edited_row = display_row()

next_match = st.button("Next (Matched)")
next_not_match = st.button("Next (Not Matched)")
back = st.button("Back")

if next_match:
    df.loc[st.session_state.row_num, "User Decision"] = "Match"
    st.session_state.row_num += 1
    display_row()

elif next_not_match:
    df.loc[st.session_state.row_num, "User Decision"] = "Unmatch"
    st.session_state.row_num += 1
    display_row()

elif back:
    st.session_state.row_num -= 1
    display_row()

final_df = convert_df(df)
if final_df is not None:
    st.markdown("You can download edited file from download button below (CSV)")
    st.download_button(
        label="Download edited data as CSV",
        data=final_df,
        file_name='edited_data.csv',
        mime='text/csv',
    )

    