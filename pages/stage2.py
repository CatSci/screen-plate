import pandas as pd
import streamlit as st
from components.filling import fill_data, color_data
import re

uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    design_df = pd.read_excel(uploaded_file, sheet_name = 'variable design CSV')
    user_df = pd.read_excel(uploaded_file, sheet_name = 'user CSV')

    # filter = st.selectbox(
    #     'How would you like to filter data?',
    #     ('conv. %', 'yield %'))

    if st.button('Fill Data'):
        updated_design_df = fill_data(design_df= design_df, user_df= user_df)
        st.write(updated_design_df.style.apply(color_data, axis = None))
