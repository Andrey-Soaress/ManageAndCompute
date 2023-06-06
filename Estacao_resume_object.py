import pandas as pd
import numpy as np
import datetime

class Resume:
    def __init__(self, path, title):

        self.special_chars = "@#$*()!;/?[]{}-_=+"
        self.letters = "abcdefghijklmnopqrstuvwjyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.log_errors = []
        self.path = path
        self.title = title
        self.table = None       
        self.metrics = None
            
    def execute_resume(self):

        self.table = pd.read_excel(self.path) 
        
        dict_rename = {}
        for idx,key in enumerate(self.table.columns):
          dict_rename[key] = self.table.loc[0].values[idx]

        self.table.rename(columns = dict_rename,inplace=True)
        dict_rename.clear()
        for idx,key in enumerate(self.table.columns[1:9]):
          dict_rename[key] = self.table.loc[1].values[idx+1]
          
        self.table.rename(columns = dict_rename,inplace=True)
        self.table.drop(index=[0,1],inplace=True)
        self.table.reset_index(inplace=True)

        self.metrics = self.table.loc[self.table.shape[0]-4:]

        self.table.drop(self.metrics.index,inplace=True)

        self.table = self.table.loc[~self.table['MÊS  '].isna().values].reset_index()

        self.table['Dia'] = self.table['MÊS  '].apply(func=lambda x : x.day).values
        self.table['Hora'] = self.table['MÊS  '].apply(func=lambda x : x.hour).values

        self.table = self.table[self.table.columns[3:]]
        self.table = self.table.loc[(~self.table.isna().values).prod(axis=1)==1]

        self.adjust_values()

        return

    def adjust_values(self):

        adjust_function = lambda x :x.strip(self.special_chars).strip(self.letters).replace(',','.')
        to_string_function = lambda x :str(x)
        
        for col in self.table.columns[0:self.table.columns.shape[0]-2]:
            try:
                self.table[col] = self.table[col].apply(to_string_function)
                self.table[col] = self.table[col].apply(adjust_function)
                self.table[col] = pd.to_numeric(self.table[col])
            except ValueError:
                self.log_errors.append(f'Type error at : {col}')

        return

    def save_table(self):

        path = ""
        temporary_path = None
        temporary_path = self.path.split("/")
            
        for i,subdir in enumerate(temporary_path[:-1]):
            path += subdir + "/"
        path += title
        
        self.table.to_csv(title,sep=';')
