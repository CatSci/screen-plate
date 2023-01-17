import numpy as np
import pandas as pd
import streamlit as st
import re
import sys, os
from exception import ScreenPlateException


def create_file(num_cols, selected_data_points, var_names) -> pd.DataFrame:
    """_summary_

    Args:
        num_cols (_type_): _description_
        selected_data_points (_type_): _description_

    Returns:
        pd.DataFrame: _description_

    Yields:
        Iterator[pd.DataFrame]: _description_
    """

    try:
        row_names = selected_data_points

        new_row_names = []
        for i in range(len(row_names)):
            for j in var_names:
                new_row_names.append(str(row_names[i]) + ' ' + j)
                # new_row_names.append(str(row_names[i]) + ' ' + 'Solvent')
            new_row_names.append(str(row_names[i]) + ' ' + 'conv. %')
            new_row_names.append(str(row_names[i]) + ' ' + 'yield %')

        matrix = []
        empty_screen_plate = []
        for i in new_row_names:
            for j in num_cols:
                empty_screen_plate.append(np.nan)
            matrix.append(empty_screen_plate)
            matrix = []
        expt_screen_plate = pd.DataFrame(matrix, index=new_row_names, columns=num_cols)

        return expt_screen_plate
    except Exception as e:
        raise ScreenPlateException(e, sys)

def find_dimensions(df):
    """_summary_

    Args:
        dataframe (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        df = df.drop(df.index[[0]])
        total_dim = list(df['Unnamed: 0'])
        temp_row = []
        temp_col = []
        for item in total_dim:
            for i in item:
                if i.isdigit():
                    temp_col += i
                else:
                    temp_row += i
        
        row = sorted(list(set(temp_row)))
        col = sorted(list(set(temp_col)))
        
        return row, col

    except Exception as e:
        raise ScreenPlateException(e, sys)

def find_row_col(dataframe, index):
    """_summary_

    Args:
        dataframe (_type_): _description_
        index (_type_): _description_

    Returns:
        _type_: _description_
    """
    # st.write(index)
    try:
        r = re.compile("([0-9]+)([a-zA-Z]+)")
        col_to_insert = r.match(index).group(1)
        row_to_insert = r.match(index).group(2)
        return row_to_insert, col_to_insert
    except Exception as e:
        raise ScreenPlateException(e, sys)

def fill_data(dataframe, screen_plate_df):
    """_summary_

    Args:
        dataframe (_type_): _description_

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """

    try:
        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe.set_index('Unnamed: 0',inplace = True)
        for i in dataframe.index:
            row_to_insert, col_to_insert = find_row_col(dataframe, i)    
            val_c = round(float(dataframe.loc[i, 'Uncorrected conv.']), 2)
            val_y = round(float(dataframe.loc[i, 'Uncorrected yield 7']), 2)

            for j in screen_plate_df.index:
                if 'conv' in j:
                    if row_to_insert in j:
                        screen_plate_df.loc[j, col_to_insert] = val_c
                elif 'yield' in j:
                    if row_to_insert in j:
                        screen_plate_df.loc[j, col_to_insert] = val_y

        return screen_plate_df
    except Exception as e:
        raise ScreenPlateException(e, sys)

def fill_variables(dataframe, col, combinations, var_names, selected_rows) -> pd.DataFrame:
    """_summary_

    Args:
        dataframe (_type_): _description_
        col (_type_): _description_
        combinations (_type_): _description_
        var_names (_type_): _description_
        selected_rows (_type_): _description_

    Raises:
        ScreenPlateException: _description_

    Returns:
        pd.DataFrame: _description_
    """
    try:
        comb_idx = 0
        comb_idx_items = 0
        for c in col:
            selected_row_idx = 0
            for r in dataframe.index:
                if selected_rows[selected_row_idx] in r:
                    if 'conv' in r:
                        comb_idx_items
                    elif 'yield' in r:
                        comb_idx_items = 0
                        comb_idx += 1
                        selected_row_idx += 1
                    else:
                        dataframe.loc[r, c] = combinations[comb_idx][comb_idx_items]
                        comb_idx_items += 1
                
        return dataframe
    except Exception as e:
        raise ScreenPlateException(e, sys)

def unique(list1):
    """_summary_

    Args:
        list1 (_type_): _description_

    Raises:
        ScreenPlateException: _description_

    Returns:
        _type_: _description_
    """
    try:
        # initialize a null list
        unique_list = []
    
        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
        # print list
        return unique_list
    except Exception as e:
        raise ScreenPlateException(e, sys)

def screen_plate_file(dataframe, var_names, combinations):
    """_summary_

    Args:
        dataframe (_type_): _description_
        var_names (_type_): _description_
        combinations (_type_): _description_

    Raises:
        ScreenPlateException: _description_

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """
    try:
        row_ids = []
        # df = pd.DataFrame(columns= ['id', var_names, 'conv. %', 'yield %'], index = range(len(combinations)))
        df = pd.DataFrame(columns= var_names, index = range(len(combinations)))
        # st.write(df)
        for col in dataframe.columns:
            # st.write(col)
            for row in dataframe.index:
                row_id = row.split(' ')[0] + col
                row_ids.append(row_id)
        
        comb_idx = 0
        for idx in df.index:
            for c in range(len(df.columns)):
                df.loc[idx,var_names[c]] = combinations[comb_idx][c]
            comb_idx += 1

        df['ID'] = unique(row_ids)
        df['conv. %'] = np.nan
        df['yield %'] = np.nan
        df.set_index('ID', inplace = True, drop = True)
        
        return df.astype(str)

    except Exception as e:
        raise ScreenPlateException(e, sys)  
