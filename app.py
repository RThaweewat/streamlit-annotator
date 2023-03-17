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

    row_num = random.choice(unfilled_rows)
    row_to_display = df.loc[row_num].to_frame().T
    edited_row = st.experimental_data_editor(row_to_display)

    return row_num, edited_row


uploaded_file = st.file_uploader("Choose your CSV file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

row_num, edited_row = display_row()

next_match = st.button("Next (Matched)")
next_not_match = st.button("Next (Not Matched)")
back = st.button("Back")

if next_match:
    df.loc[row_num, "User Decision"] = "Match"
    row_num, edited_row = display_row()

elif next_not_match:
    df.loc[row_num, "User Decision"] = "Unmatch"
    row_num, edited_row = display_row()

elif back:
    row_num, edited_row = display_row()

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



