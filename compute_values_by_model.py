import statsmodels.api as sm
import statsmodels.formula.api as smf
from keras.models import Sequential
from keras.layers import Dense,Input,Dropout,SimpleRNN
from sklearn.ensemble import RandomForestRegressor
from keras import models
import pandas as pd
import numpy as np

def compute(model,data_test,component):

  dist = lambda x,y: np.sqrt(np.sum((x-y)**2))

  predicts_column = []
  index = []

  if model['method'] == 'limits':
    for m in model['models']:
      data = data_test.loc[data_test[component+'_moqa']<model['models'][m]['sup']]
      data = data.loc[data[component+'_moqa']>=model['models'][m]['inf']]
      s = model['models'][m]['modelo'].predict(sm.add_constant(data))
      predicts_column.extend(s.values)
      index.extend(s.index.values)

  elif model['method'] == 'proximity':
    for m in model['models']:
      idx_to_this_model = []
      for i in data_test.index:
        min = np.infty
        mod_atual = None
        for m_ in model['models']:
          d = dist(model['models'][m_]['center'],data_test.loc[i][model['models'][m_]['var']])
          if d < min: 
            min = d
            mod_atual = m_
        if mod_atual == m: 
          idx_to_this_model.append(i)

      data = data_test.loc[idx_to_this_model]
      predicts_column.extend(model['models'][m]['modelo'].predict(sm.add_constant(data)))
      index.extend(idx_to_this_model)
  
  elif model['method'] == 'RF':
    predicts_column = model['models']['modelo'].predict(data_test[model['models']['var']].values)
    index = np.arange(0,data_test.shape[0])
  
  elif model['method'] == 'NN':
    predicts_column = model['models']['modelo'].predict(data_test[model['models']['var']].values).reshape(1,-1)[0]
    index = np.arange(0,data_test.shape[0])

  table = pd.DataFrame(index=index,data=predicts_column,columns=[component+'_model'])

  table = pd.merge(data_test,table,left_index=True,right_index=True)

  return table
