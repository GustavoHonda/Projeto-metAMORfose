import json 
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import warnings
import csv


def get_files(path,selected = []):
    files = []
    for arquivo in os.listdir(path):
        if arquivo.endswith(".csv"):
            if selected != []:
                if arquivo.replace(".csv","") in selected:
                    files.append(os.path.join(path, arquivo))
            else:
                files.append(os.path.join(path, arquivo))
    return sorted(files)

def get_dataframes(files,list=[]):
    if files == []:
        print("Error: null files for dataframe")
        exit(0)
    dfs = []
    df_names = []
    for loop,fi in enumerate(files):
        name = os.path.basename(fi).replace(".csv","")
        df_names.append(name)
        df = pd.read_csv(fi, index_col=0)
        dfs.append(df)
    # labels = [element.replace(".","_") for element in df.index]
    return df_names, dfs

def get_columns(df):
    return df.columns

def get_dif_values(df, column):
    return df[column].unique()
    
def set_header(df):
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    return df

def drop_nan(df):
    df = df.dropna(axis=1, how='all')
    return df

categories = ['Psicoterapia', 'Nutrição', 'Terapia', 'Personal trainer',
       'Terapia holística', 'Clínico geral', 'Outros', 'Psiquiatria',
       'Terapia de psicologia ou psicanálise', 'Ginecologista',
       'Geriatra ou Gerontólogo']




files = get_files("../csv/")
df_names, dfs = get_dataframes(files)
df = dfs[2]

df = df.reset_index()
set_header(df)
df = drop_nan(df)

df["categorie"] = df["categorie"].str.split(",")
df = df.explode('categorie')
df['categorie'] = df['categorie'].str.replace("Médico","", regex=True)
df['categorie'] = df['categorie'].str.replace(":","", regex=True)
df['categorie'] = df['categorie'].str.strip()

df['datetime'] = pd.to_datetime(df['time'], dayfirst=True)
df['datetime'] = df['datetime'].dt.strftime(f'%Y/%m/%d %H:%M:%S')
df[['date','time']] = df['time'].str.split(" ", expand= True )


def date_plot():
    '''
    var = ['time','date','datetime']
    precision = ['xxMin','H','D','W','M','Y']
    '''
    var = 'date'
    precision = '7D'
    df[var] = pd.to_datetime(df[var])
    frequencie = df[:]
    frequencie.set_index(var)
    frequencie = df.resample(precision, on=var).size()
    print(frequencie)
    plt.figure(figsize=(10, 5))
    frequencie.plot(kind='line', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.title('Frequency of Dates Over Continuous Days')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def weekday_plot():
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['day_of_week'] = df['datetime'].dt.day_name()
    frequencie = df['day_of_week'].value_counts()
    frequencie.plot()
    plt.show()
    

def categorie_plot():
    frequencie = df['categorie'].value_counts()
    print(frequencie.index)
    frequencie.sort_values(ascending=True).plot(kind='barh')
    # frequencie.plot(kind='pie',autopct='%1.1f%%')
    plt.title('Categorias mais requisitadas')
    plt.ylabel('Contagem')
    plt.show()

categorie_plot()
date_plot()
weekday_plot()