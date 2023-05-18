import pickle
from keras.models import Sequential
from keras.layers import Dense,Input,Dropout,SimpleRNN,LSTM
from keras.optimizers import Adam
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import load_model

def load_my_model(paths):
    paths_quantity = len(paths)
    
    if paths_quantity == 0: 
        raise Exception('No path files to read')
        return
    
    if paths_quantity == 2:
        return load_h5_model(path)
    else paths_quantity == 1:
        return load_bin_model(path)

def load_bin_model(path):
    model_arq = open(path,'rb')
    model = None
    
    try:
        model = pickle.load(model_arq)
    except EOFError:
        if model != None: print("The model has been loaded!")
    model_arq.close()
    
    return model

def load_h5_model(path)
    model = load_bin_model(path[0])
    model['models']['modelo'] = load_model(path[1])
    
    return model    

if __name__ == '__main__':
    raise Exception('This script should not be used directly')
