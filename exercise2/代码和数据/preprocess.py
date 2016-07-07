#-*- coding: utf-8 -*- 
import csv
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

# get transaction mode
def get_transaction_item(full_item, bool_item):
    ret = []
    for i in range(len(full_item)):
        if bool_item[i]=='yes':
            ret.append(full_item[i])
    return ret

def preprocess():
    ret = []
    attr = ['a1','a2','a3','a4','a5','a6','d1','d2']
    data = pd.read_csv('data.csv')
    a1 = data['a1']
    a1[a1>37.5]='yes'
    a1[a1<=37.5]='no'
    data['a1'] = a1
    for i in range(len(data)):
        trans = get_transaction_item(attr, data.loc[i])
        ret.append(trans)
        print (trans)
    return ret


