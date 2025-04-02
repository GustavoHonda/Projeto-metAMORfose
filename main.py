import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import warnings


def get_files(path,selected = []):
    '''
    Select all csv files in path.
    
    args:
        path (str): relative path to datasets directory Ex:"./csv".
        selects ([str]): specific files to be selected in datasets directory.
    
    returns:
        [str]: list of file paths to selected datasets.
    
    '''
    
    files = []
    for arquivo in os.listdir(path):
        if arquivo.endswith(".csv"):
            if selected != []:
                if arquivo.replace(".csv","") in selected:
                    files.append(os.path.join(path, arquivo))
            else:
                files.append(os.path.join(path, arquivo))
    return sorted(files)

def get_dataframes(files):
    '''
    Get dataframes from files.
    
    args:
        files ([str]): full path to csv datasets files.
    
    returns:
        [str], [Dataframe]: list of dataframe names and list of dataframes.
    '''
    
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
    return df_names, dfs
    
def set_header(df):
    '''
    Set first row of dataframse as headers.
    
    args:
        df (Dataframe): Dataframe to be modified.
    
    returns:
        Dataframe: Modified Dataframe.
    '''
    
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    return df

def drop_nan(df):
    '''
    Drop all rows with Nan value in any column.
    
    args:
        df (Dataframe): Dataframe to be modified.
        
    return:
        Dataframe: Modified Dataframe.
    '''
    
    df = df.dropna(axis=1, how='all')
    return df

def date_plot(df, column = 'date', precision = '7D'):
    '''
    Plot continuos sampled date chart of given Dataframe.
    
    args:
        df (Dataframe): Dataframe with date column.
        column (str): Name of date column.
        precision (str): Precision of sampling. Ex: 'xxMin','H','D','W','M','Y'

    return:
        None.
    '''
    
    df[column] = pd.to_datetime(df[column])
    frequencie = df[:]
    frequencie.set_index(column)
    frequencie = df.resample(precision, on=column).size()
    plt.figure(figsize=(10, 5))
    frequencie.plot(kind='line', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.title('Frequency of Dates Over Continuous Days')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def weekday_plot(df, column= 'datetime'):
    '''
    Plot weekly frequencie of given Dataframe column.
    
    args:
        df (Dataframe): Dataframe with date column.
        column (str): Name of date column.
        precision (str): Precision of sampling. Ex: 'xxMin','H','D','W','M','Y'

    return:
        None.
    '''
    
    df[column] = pd.to_datetime(df[column])
    df['day_of_week'] = df[column].dt.day_name()
    frequencie = df['day_of_week'].value_counts()
    frequencie = frequencie.reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    frequencie.index = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']
    frequencie.plot()
    plt.ylabel('Frequência')
    plt.xlabel('Dia da semana')
    plt.title('Frequência pelo dia da semana')
    plt.show()
    

def categorie_plot(df, column):
    '''
    Plot categorie frequencie of given Dataframe column.
    
    args:
        df (Dataframe): Dataframe with categorie column.
        column (str): Name of categorie column.

    return:
        None.
    '''
    
    frequencie = df[column].value_counts()
    frequencie.sort_values(ascending=True).plot(kind='barh')
    # frequencie.plot(kind='pie',autopct='%1.1f%%')
    plt.title('Gráfico de categorias')
    plt.ylabel('Categorias')
    plt.ylabel('Contagem')
    plt.show()


def preprocess_dfclient(df):
    '''
    Preprocess Client Dataframe.
    
    args:
        df (Dataframe): Client Dataframe
    
    return:
        Dataframe: Preprocessed Dataframe.
    
    '''
    
    df = df.reset_index()
    # set_header(df)
    df = drop_nan(df)

    # Categorie column
    df["categorie"] = df["categorie"].str.split(",")
    df = df.explode('categorie')
    df['categorie'] = df['categorie'].str.replace("Médico","", regex=True)
    df['categorie'] = df['categorie'].str.replace(":","", regex=True)
    df['categorie'] = df['categorie'].str.strip()

    # Datetime column
    df['datetime'] = pd.to_datetime(df['time'], dayfirst=True)
    df['datetime'] = df['datetime'].dt.strftime(f'%Y/%m/%d %H:%M:%S')
    df[['date','time']] = df['time'].str.split(" ", expand= True )

    return df

def preprocess_dfprofissional(df):
    '''
    Preprocess Professional Dataframe.
    
    args:
        df (Dataframe): Professional Dataframe
    
    return:
        Dataframe: Preprocessed Dataframe.
    
    '''
    
    return df




def main():

    files = get_files("../csv/")
    df_names, dfs = get_dataframes(files)

    # Print Client charts
    df_client = preprocess_dfclient(df=dfs[3])
    categorie_plot(df=df_client, column='categorie')
    date_plot(df=df_client, column='date', precision='W')
    weekday_plot(df=df_client, column='datetime')

    # Print Professional charts
    df_profissional = preprocess_dfprofissional(df=dfs[0])
    categorie_plot(df=df_profissional,column='area')


if __name__ == '__main__':
    main()
