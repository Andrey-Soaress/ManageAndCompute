import pickle
from keras.models import Sequential
from keras.layers import Dense,Input,Dropout,SimpleRNN,LSTM
from keras.optimizers import Adam
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import load_model

def load_model(path,type_arq):
    if type_arq == 'h5':
        return load_bin_model(path)
    elif type_arq == 'bin':
        return load_h5_model(path)

def load_bin_model(path):
    model = None
    try:
        model = pickle.load(path,'r')
    except EOFError:
        if model != None: print("The model has been loaded!")

    return model

def load_h5_model(path)
    model = load_model(path)
    return model    

if __name__ == '__main__':
    raise Exception('This script should not be used directly')
