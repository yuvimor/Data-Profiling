import streamlit as st 
import pandas as pd 
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os

st.set_page_config(page_title="Data Profiler", layout="wide")

def get_filesize(file):
    filesize_bytes = sys.getsizeof(file)
    filesize_mb = filesize_bytes / (1024*1024)
    return filesize_mb

def get_file_ext(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext not in ('.xlsx','.csv'):
        return False
    else:
        return ext

def read_excel():
    global df
    df = xl.parse(sheet_name=sheet_name)

with st.sidebar:
    uploaded_file = st.file_uploader('Upload .csv, .xlsx file not exceeding 10MB')
    
    #filesize = uploaded_file.raw.
    #st.write("filesize is =",filesize)
    
    st.markdown('---')
    st.text('Mode of Operation')
    if uploaded_file is not None:                    
        minimal= st.checkbox("Do you want minimal report ?")
        #print(minimal)
        display_mode = st.radio('Display Mode',('Primary','Dark','Orange'))
        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False
    


if uploaded_file is not None:
    if get_filesize(uploaded_file) > 10:
        message = f""""
        Uploaded File size = {get_filesize}
        But maximum file size can be uploaded is 10 MB
        """
        st.error(message)
    else:
        st.success("File size less then 10 MB")
    
        ext = get_file_ext(uploaded_file)
        if ext:
            if ext == '.xlsx':
                xl = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl.sheet_names)
                sheet_name = st.sidebar.selectbox('Select the sheets',
                                                  options=sheet_tuple)
                df = xl.parse(sheet_name=sheet_name)
                print("sheet_name = ",sheet_name)
                
                sucess = True
            elif ext == '.csv':
                df = pd.read_csv(uploaded_file)
                sucess = True
        else:
            st.error('Kindly upload only csv and xls file')
            sucess = False

    if sucess:                        
        with st.spinner('Please wait while processing'):
            #print(minimal)    
            pr = ProfileReport(df,
                            minimal=minimal,
                            explorative=False,
                            dark_mode=dark_mode,
                            orange_mode=orange_mode
                            )

        st_profile_report(pr)
else:
    st.title('Data Profiler')
    st.info('Upload your data (.csv or .xlsx) in the sidebar for detail report')

    
