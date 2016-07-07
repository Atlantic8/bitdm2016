#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def format_key(key):
    ret = ''
    if type(key) != tuple:
        return str(key)
    elif len(key) == 1:
        return format_key(key[0])
    else:
        ret = format_key(key[0])
        for i in range(1,len(key)):
            ret = ret + ',' + format_key(key[i])
    return ret

def format_rule(rule):
    #print(rule)
    return format_key(rule[0])+'->'+format_key(rule[1])

# dic is a dictionary, x is a number
def plot_scatter(dic, x):
    key = dic.keys()
    value = dic.values()
    title = 'frequent item '+str(x)+' count'
    plt.title(title)
    plt.scatter(xrange(len(key)), value)
    plt.xticks(xrange(len(key)),map(format_key, key),rotation=90)

    plt.savefig('fig\\'+title+'.png')
    plt.show()

# frequent histogram
def hist_statistical(data, title):
    plt.title(title)
    plt.hist(data)
    plt.savefig('fig\\'+title+'.png')
    plt.show()
    
def plot_bar(rules, data, title):
    plt.title(title)
    plt.xticks(xrange(len(data)),map(format_rule, rules),rotation=90)
    plt.bar(xrange(len(data)), data, color = 'g')
    plt.savefig('fig\\'+title+'.png')
    plt.show()