import pandas as pd
import streamlit as st
import re
import math

def split(string):
    temp = re.compile("([a-zA-Z]+)([0-9]+)")
    res = temp.match(string).groups()

    return res


def fill_data(design_df, user_df):
    # design_df.set_index('Unnamed: 0')
    design_df = design_df.rename(columns={"Unnamed: 0": "index"})
    design_df = design_df.set_index('index')

    for i in range(user_df.shape[0]):
        id = user_df.loc[i, 'ID']
        
        letter, num = split(id)
        conv_val = user_df.loc[i, 'conv. %']
        yield_val = user_df.loc[i, 'yield %']
        if math.isnan(conv_val) == False and math.isnan(yield_val) == False:
            row_conv = letter + ' ' + 'conv. %'
            row_yield = letter + ' ' + 'yield %'
            
            if row_conv and row_yield in design_df.index:
                design_df.loc[row_conv, str(num)] = conv_val
                design_df.loc[row_yield, str(num)] = yield_val
    

    return design_df



# def color_data(val):
#     # st.write(type(val))
#     matches = re.findall('[0-9]', val)
#     if matches:
#         # st.write(val)
#         if float(val) > 70.0:
#             color = 'green'
#         else:
#             color = 'lightcoral'
    
#         return 'color: %s' %color
#     else:
#         # st.write(type(val))
#         return 'color: %s' %'grey'

# conv > 90 and yield > 75 ------> color = green
# conv > 90 and 60 < yield < 75----> color = yellow
# conv < 90 and 0.1 < yield < 60----> color = pink


# def color_data(x):
#     c1 = f'background-color: #94C973;' # green
#     c2 = f'background-color: #F8EA8C;' # yellow
#     c3 = f'background-color: #FFC5D0;' # pink
#     c4 = f'background-color: #BDC3CB' # gray
#     c5 = f'background-color: white;' # white


#     df1 = pd.DataFrame('', index = x.index, columns = x.columns)
#     for i in x.columns:
#         for j in x.index:
#             if 'yield' in j:
#                 val = x.loc[j, i]
#                 if float(val) > 75.0:
#                     df1.loc['A conv. %', i] = c1
#                     df1.loc[j,i] = c1
#                 elif 60.0 <= float(val) < 75.0:
#                     df1.loc[j,i] = c2
#                 elif 0.1 < float(val) < 60.0:
#                     df1.loc[j,i] = c3
#                 else:
#                     df1.loc[j,i] = c4
#             else:
#                 df1.loc[j,i] = c5

#     return df1



def color_data(x):
    c1 = f'background-color: #94C973;' # green
    c2 = f'background-color: #F8EA8C;' # yellow
    c3 = f'background-color: #FFC5D0;' # pink
    c4 = f'background-color: #BDC3CB' # gray
    c5 = f'background-color: white;' # white

    df1 = pd.DataFrame('', index = x.index, columns = x.columns)
    for col in x.columns:
        index_list = list(x.index)
        for idx in range(len(index_list)):
            if 'yield' in index_list[idx]:
                conv_val = x.loc[index_list[idx - 1], col]
                yield_val = x.loc[index_list[idx], col]
                if float(conv_val) > 90.0 and float(yield_val) > 75.0:
                    df1.loc[index_list[idx], col] = c1
                    df1.loc[index_list[idx - 1], col] = c1
                elif float(conv_val) > 90.0 and 60.0 < float(yield_val) < 75.0:
                    df1.loc[index_list[idx], col] = c2
                    df1.loc[index_list[idx - 1], col] = c2
                elif float(yield_val) < 0.1:
                    df1.loc[index_list[idx], col] = c4
                    df1.loc[index_list[idx - 1], col] = c4
                elif float(conv_val) < 90.0 or 0.1 < float(yield_val) < 60.0:
                    df1.loc[index_list[idx], col] = c3
                    df1.loc[index_list[idx - 1], col] = c3
                
            else:
                df1.loc[index_list[idx], col] = c5
    
    return df1

    
            
                 