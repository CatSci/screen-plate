import numpy as np
import pandas as pd
from openpyxl import load_workbook

import streamlit as st
import itertools
from components.design import create_file, find_dimensions, fill_data, fill_variables, screen_plate_file
from utils.utils import create_multisheet_csv

st.title('Screen Plating')

total_var = st.text_input('Please enter number of variables', value = 3, placeholder= 'Metal')
elements = []
if not total_var:
    st.error('Cannot leave empty field')
else:
    var_names = []
    unique_key = 0
    for i in range(int(total_var)):
        unique_key += 1
        var_name = st.text_input('Please enter name of variable', placeholder= 'Metal', key = f"name{unique_key}")
        var_names.append(var_name)
        if var_name:
            var_count = st.text_input('Please enter number of ' + var_name, key = f"count{unique_key}")
            sub_variable = st.text_input('Please enter names of ' + var_name, placeholder= 'Pd,Ni', key = f"sub_name{unique_key}")
            elements.append(sub_variable.split(','))


if elements:
    comb = list(itertools.product(*elements))
    # st.write(comb)

data_file = st.file_uploader('Choose a file')


if data_file is not None:     
    df = pd.read_excel(data_file, sheet_name= "UPLC Data (iClass)").astype(str)
    row, col = find_dimensions(df)
    selected_rows = st.multiselect('Select Rows',
        row)
    if st.button('Create Screen Plating'):
        expt_screen_plate = create_file(col, sorted(selected_rows), var_names)
        # screen_plate = fill_data(df, expt_screen_plate)


        variable_design_df = fill_variables(expt_screen_plate, col, comb, var_names, sorted(selected_rows)).astype(str)
        # st.dataframe(variable_design_df)
        user_df = screen_plate_file(variable_design_df, var_names, comb) 
        # st.write(user_df)


        file = create_multisheet_csv(variable_design_df, user_df)
        st.download_button(label='📥 Download',
                                data=file ,
                                file_name= 'design.xlsx')
        
        


        
# working files
#screen plate 1  
#screen plate 2
#screen plate 
#screen plate 3 working except F row


#screen plate 4 issue in combinations
