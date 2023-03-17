import streamlit as st
import pandas as pd
import random

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")


@st.cache
def convert_df(dataframe: pd.DataFrame):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return dataframe.to_csv().encode('utf-8')


def display_row():
    unfilled_rows = df[df["User Decision"] == ""].index.tolist()

    if not unfilled_rows:
        st.write("All done!")
        return None

    if 'row_num' not in st.session_state or st.session_state.row_num not in unfilled_rows:
        st.session_state.row_num = random.choice(unfilled_rows)

    row_to_display = df.loc[st.session_state.row_num].to_frame().T
    edited_row = st.experimental_data_editor(row_to_display)
    st.session_state.edited_row = edited_row
    return edited_row


uploaded_file = st.file_uploader("Choose your CSV file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

df['User Decision'] = ""
df['Row Number'] = range(len(df))

edited_row = display_row()

def update_row_state():
    display_row()

next_match = st.button("Next (Matched)")
next_not_match = st.button("Next (Not Matched)")
back = st.button("Back")

if next_match:
    df.loc[st.session_state.row_num, "User Decision"] = "Match"
    update_row_state()

elif next_not_match:
    df.loc[st.session_state.row_num, "User Decision"] = "Unmatch"
    update_row_state()

elif back:
    st.session_state.row_num -= 1
    update_row_state()

final_df = convert_df(df)
if final_df is not None:
    st.markdown("You can download edited file from download button below (CSV)")
    st.download_button(
        label="Download edited data as CSV",
        data=final_df,
        file_name='edited_data.csv',
        mime='text/csv',
    )

filled_rows = df[df["User Decision"] != ""].count()["User Decision"]
unfilled_rows = df[df["User Decision"] == ""].count()["User Decision"]

st.write(f"Filled rows: {filled_rows}")
st.write(f"Unfilled rows: {unfilled_rows}")


