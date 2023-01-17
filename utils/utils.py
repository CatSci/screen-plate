import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

# @st.cache
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')

def create_multisheet_csv(df1, df2):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df1.to_excel(writer, index=True, sheet_name='variable design CSV')
    df2.to_excel(writer, index=True, sheet_name='user CSV')

    writer.save()
    return output.getvalue()
    
    