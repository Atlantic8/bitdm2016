#-*- coding: utf-8 -*-
from preprocess import preprocess
from visualization import hist_statistical,plot_scatter,plot_bar

def count(data, item):
    cnt = 0
    for trans in data:
        if set(item).issubset(set(trans)) == True:
            cnt = cnt + 1 
    return cnt

def key_division(key):
    cond = []
    conc = []
    for x in key:
        if x < 'd':
            cond.append(x) 
        else: 
            conc.append(x)
    return tuple([tuple(cond), tuple(conc)])

def frequent_item_1(data):
    dic = {}
    total_count = len(data)
    for attr in attrs:
        dic[attr] = count(data, [attr])
    
    # print frequent item 1
    print('frequent item 1')
    for key,value in dic.items():
        if value >= thres:
            print('key: '+key+", value: "+str(value))
        else:
            dic.pop(key)
    print('\n')
    return dic

def frequent_item_2(data, dic1):
    dic = {}
    dic1_key = dic1.keys()
    for a in dic1_key:
        for b in dic1_key:
            if a <= b:
                continue
            dic[(a,b)] = count(data, [a,b])
    
    # print frequent item 2
    print('frequent item 2')
    for key,value in dic.items():
        if value >= thres:
            print('key: ',key, ' value: '+str(value))
        else:
            dic.pop(key)
    print('\n')
    return dic

def frequent_item_3(data, dic1, dic2):
    dic = {}
    redundant_set = []
    dic1_key = set(dic1.keys())
    dic2_key = set(dic2.keys())
    for k2 in dic2_key:
        for k1 in dic1_key:
            if tuple([k2[0],k1]) not in dic2_key or tuple([k2[1],k1]) not in dic2_key or set(list(k2)+[k1]) in redundant_set:
                continue
            new_key = key_division(tuple(list(k2)+[k1]))
            if len(new_key[1]) == 0:
                continue
            tmp = count(data, list(k2)+[k1])
            if tmp < 10:
                continue
            dic[new_key] = tmp
            redundant_set.append(set(list(k2)+[k1]))
    
    # print frequent item 3
    print('frequent item 3')
    for key,value in dic.items():
        if value >= thres:
            print('key: ',tuple(list(key[0])+list(key[1])), ' value: '+str(value))
        else:
            dic.pop(key)
    print('\n')
    return dic

def export_association_rule(dic1,dic2,dic3):
    for key in dic3.keys():
        x = dic1[key[0][0]] if len(key[0])==1 else dic2[key[0]]
        y = dic1[key[1][0]] if len(key[1])==1 else dic2[key[1]]
        sup = dic3[key] * 1.0 / leng
        support.append(sup)
        conf = dic3[key] * 1.0 / x
        confidence.append(conf)
        expect_confidence = y *1.0 /leng
        lif = conf / expect_confidence
        lift.append(lif)
        #print(key[0],' -> ',key[1],'support: '+str(support)+'  confidence: '+str(confidence)+'  lift: '+str(lift))
        print('%s -> %s, support: %1.6f  confidence: %1.6f  lift: %1.6f' % (str(key[0]), str(key[1]), sup, conf, lif))

def visualization():
    '''
    plot_scatter(dic1, 1)
    plot_scatter(dic2, 2)
    plot_scatter(dic3, 3)
    '''
    plot_bar(rule, support, 'rule-support figure')
    plot_bar(rule, confidence, 'rule-confidence figure')
    plot_bar(rule, lift, 'rule-lift figure')

if __name__=="__main__":
    thres = 10  # filter threshold
    attrs = ['a1','a2','a3','a4','a5','a6','d1','d2']
    print('-----------------------pre-process data----------------------')
    data = preprocess()
    leng = len(data)
    print('-----------------------data preprocess is done----------------------')
    print('\n')
    print('-----------------------counting frequent item starts----------------------')
    dic1 = frequent_item_1(data)
    dic2 = frequent_item_2(data, dic1)
    dic3 = frequent_item_3(data, dic1, dic2)
    print('-----------------------counting frequent item done----------------------')
    print('\n')
    print('-----------------------export association rule----------------------')
    rule = dic3.keys()
    support = []
    confidence = []
    lift = []
    export_association_rule(dic1, dic2, dic3)
    print('-----------------------export association rule done----------------------')
    visualization()
    
    