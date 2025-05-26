import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from get_data import open_professional, open_respostas
import warnings

# Erros/implementações que tem pra fazer/corrigir nesse módulo:


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
    
    df[column] = pd.to_datetime(df[column], dayfirst=True)
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
    

def area_plot(df, column):
    '''
    Plot area frequencie of given Dataframe column.
    
    args:
        df (Dataframe): Dataframe with area column.
        column (str): Name of area column.

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


def main():

    df_resposta = open_respostas()
    df_professional = open_professional()

    # Print resposta charts
    area_plot(df=df_resposta, column='area')
    date_plot(df=df_resposta, column='date', precision='W')
    weekday_plot(df=df_resposta, column='datetime')

    # Print Professional charts
    area_plot(df=df_professional,column='area')


if __name__ == '__main__':
    main()
