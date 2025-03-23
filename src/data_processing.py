import numpy as np
import pandas as pd

def load_and_clean_data(file_path):
    retail_data=pd.read_excel(file_path)

    retail_data_clean=retail_data.dropna(subset=['CustomerID'])
    retail_data_clean["InvoiceDate"]=pd.to_datetime(retail_data_clean['InvoiceDate'])
    retail_data_clean=retail_data_clean[~retail_data_clean["InvoiceNo"].astype(str).str.contains('C')]
    retail_data_clean['TotalPrice']=retail_data_clean['Quantity']*retail_data_clean["UnitPrice"]

    return retail_data_clean
