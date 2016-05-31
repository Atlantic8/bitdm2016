# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import csv
from math import isnan,sqrt
import matplotlib.pyplot as plt
import pylab
import scipy.stats as stats

numeric_attr = []
non_numeric_attr = []
type_data = []

def nan_convert(x):
    if x == 'XXXXXXX':
        return np.nan
    else:
        return float(x)

def distance(a, b):
    dist = 0.0
    for i in range(3,len(a)):
        if isnan(a[i])==True and isnan(b[i])==True:
            return 1000000
        if isnan(a[i])==True or isnan(b[i])==True:
            continue
        dist = dist + (a[i]-b[i])*(a[i]-b[i])
    return sqrt(dist)

# use b to patch a, from index 3
def patch(a, b):
    ret = []
    ret.append(a[0])
    ret.append(a[1])
    ret.append(a[2])
    for i in range(3,len(a)):
        if isnan(a[i]) == True:
            ret.append(b[i])
        else:
            ret.append(a[i])
    print ret
    return ret

# use b to patch a
def patch2(a, b):
    ret = []
    for i in range(len(a)):
        if isnan(a[i]) == True:
            ret.append(b[i])
        else:
            ret.append(a[i])
    return ret

def find_second_big(a):
    max_value, index = -1, 0
    for i in range(len(a)):
        if max_value < a[i] and a[i] < 1:
            max_value = a[i]
            index = i
    return index

def replace_default(data, type):
    if type == 0:
        for attr in numeric_attr:
            # data[attr].replace('XXXXXXX','NaN')
            data[attr] = Series(map(nan_convert, list(data[attr])))
    elif type == 1: # delete missing value
        return data.dropna()
    elif type == 2:
        for attr in numeric_attr:
            element, num = 0.01, -1
            tmp = list(data[attr])
            # find the one with highest frequency.
            for x in data[attr].unique():
                if x == np.nan:
                    continue
                elif tmp.count(x) > num:
                    num = tmp.count(x)
                    element = x
            data[attr] = data[attr].replace(np.nan, element)
        return data
    elif type == 3:
        data1 = data[numeric_attr]
        cor_data = data1.corr()
        for attr in numeric_attr:
            tmp = pd.isnull(data[attr])
            if True not in list(tmp):
                continue
            index = find_second_big(cor_data[attr])
            data[attr] = patch2 (data[attr], data[numeric_attr[index]])
        return data
    elif type == 4:
        for i in range(len(data)):
            tmp = pd.isnull(data.iloc[i])
            if True not in list(tmp):
                continue
            else:
                min_dis, min_index = 10000000.0, 0
                for j in range(len(data)):
                    if i == j:
                        continue
                    else:
                        dis = distance(data.iloc[i], data.iloc[j])
                        if min_dis > dis:
                            min_dis = dis
                            min_index = j
                data.iloc[i] = patch(data.iloc[i], data.iloc[min_index])
        return data            

# 缺失值统计
def missing_count(data):
    print ('count missing value')
    for attr in numeric_attr:
        num = 0
        for x in data[attr]:
            if isnan(x) == True:
                num = num + 1
        print (attr, num)


# 标称属性数据摘要
def data_abstract(feature, unique_feature):
    for s in unique_feature:
        print (s,feature.count(s))

# 数值属性数据摘要
def data_abstract_numeric(data):
    # print ('default value count: ', list(feature).count('XXXXXXX'))
    # feature = feature.replace('XXXXXXX', '');
    # data = Series(map(lambda x: float(x), feature));
    print ('max value: ', data.max())
    print ('min value: ', data.min())
    print ('median value: ', data.median())
    print ('quantile(0.25): ', data.quantile(0.25))
    print ('quantile(0.75): ', data.quantile(0.75))

def plot_histogram(data1, title):
    plt.title(title)
    plt.hist(data1)
    plt.savefig('fig\\'+title+'hist.png')
    plt.show()
    # draw qq graph
    stats.probplot(data1, dist="norm", plot=pylab)
    pylab.savefig('fig\\'+title+'qq.png')
    pylab.show()

def plot_box(data1,title):
    plt.title(title)
    plt.boxplot(data1, notch=False, sym='rs', vert=True)
    # plt.show(data1.plot(kind = 'box'))
    plt.savefig('fig\\'+title+'.png')
    plt.show()

# target is season or size or speed

def plot_conditional_box(data, unique_feature, title1, title2):
    plt.title(title1+' & '+title2)
    res = []
    for uf in unique_feature:
        res.append(list(data[data[title1] == uf][title2]))
    plt.boxplot(res, notch=False, sym='rs', vert=True)
    plt.xticks([y+1 for y in range(len(res))], list(unique_feature))
    plt.savefig('fig\\'+title1+' & '+title2+'.png')
    plt.show()
    

def visualization(data):
    # abstract for non-numeric data.
    print ('count non-numeric attributes value')
    season = list(data['season'])
    data_abstract(season, Series(season).unique())
    size = list(data['size'])
    data_abstract(size, Series(size).unique())
    speed = list(data['speed'])
    data_abstract(speed, Series(speed).unique())

    # abstract for numeric data.
    print ('count numeric attributes value')
    for attr in numeric_attr:
        print ('attribute: '+attr)
        data_abstract_numeric(data[attr])

    # plot histogram
    for attr in numeric_attr:
        plot_histogram(data[attr], attr)

    # plot plot_box
    for attr in numeric_attr:
        plot_box(data[attr], attr)
    #plot_box(data[['mxPH','mnO2','Cl','NO3','NH4','oPO4','PO4','Chla']],'plot box')
    
    # plot conditional plot_box
    for attr in non_numeric_attr:
        unique_attr = data[attr].unique()
        for attr2 in type_data:
            plot_conditional_box(data[[attr, attr2]], unique_attr, attr, attr2)
            

# switch space to ',', so that we can read .csv directly

data = pd.read_csv('Analysis.csv');
column = list(data.columns)
non_numeric_attr = column[0:3]
numeric_attr = column[3:11]
type_data = column[11:]
replace_default(data, 0)
missing_count(data)
# print (data[numeric_attr].corr())

# delete operation
data1 = data.copy()
data1 = replace_default(data1, 1)
visualization(data1)
data1.to_csv('Analysis1.csv')
del data1
 
# most frequent replacement
data1 = data.copy()
data1 = replace_default(data1, 2)
visualization(data1)
data1.to_csv('Analysis2.csv')
del data1

# column correlation replacement
data = data.drop([61,198])
data.index = range(len(data))
data1 = data.copy()
data1 = replace_default(data1, 3)
print (data1)
visualization(data1)
data1.to_csv('Analysis3.csv')
del data1

# row correlation replacement
data1 = data.copy()
data1 = replace_default(data1, 4)
visualization(data1)
data1.to_csv('Analysis4.csv')
del data1