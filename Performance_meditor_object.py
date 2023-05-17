from sklearn.metrics import r2_score,mean_squared_error
import pandas as pd
import numpy as np

class Performance_meditor:

  def __init__(self,table,component):
    self.table = table
    self.component = component
    self.table_of_metrics = None
    self.dictionary_of_metrics = {}

    self.init_dict()

    self.init_table_of_metrics()

  def init_dict(self):
    metric_label = ['R2','RMSE','NRMSE','STD DEV']
    for m in metric_label: 
      self.dictionary_of_metrics[m] = None

    self.calculate_metrics()

  def metrics(self):
    R2 = lambda true,pred: r2_score(true,pred)
    RMSE = lambda true,pred: mean_squared_error(true,pred,squared=False)
    NRMSE = lambda true,pred: (mean_squared_error(true,pred)*true.shape[0])/np.sum(true**2)
    STD_dev = lambda true,pred: np.std(pred-true)

    return {'R2':R2,'RMSE':RMSE,'NRMSE':NRMSE,'STD DEV':STD_dev}

  def calculate_metrics(self):
    mtrcs = self.metrics()
    for metric in self.dictionary_of_metrics:
      self.dictionary_of_metrics[metric] = []
      self.dictionary_of_metrics[metric].append(mtrcs[metric](self.table[self.component+'_est'].values,
                                                              self.table[self.component+'_model'].values))
      self.dictionary_of_metrics[metric].append(mtrcs[metric](self.table[self.component+'_est'].values,
                                                              self.table[self.component+'_moqa'].values))
      
      s = ''
      if self.dictionary_of_metrics[metric][1] > 0:
        s = str(round(np.abs((self.dictionary_of_metrics[metric][0]-self.dictionary_of_metrics[metric][1])/self.dictionary_of_metrics[metric][1])*100,2))+'%'
      else:
        s = 'N/A'

      self.dictionary_of_metrics[metric].append(s)
      
    print('\nMedições realizadas!\n')
  
  def init_table_of_metrics(self):
    self.table_of_metrics = pd.DataFrame(data = self.dictionary_of_metrics,
                                          index=['Model','Moqa','Rel'])
