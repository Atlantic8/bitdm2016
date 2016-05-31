##### 作者：曹文强
- preprocess.py是源程序
源程序需要导入一些python常用的科学计算与绘图包
```python
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import csv
from math import isnan,sqrt
import matplotlib.pyplot as plt
import pylab
import scipy.stats as stats
```
- Analysis1.csv: 删除缺失值的结果
- Analysis2.csv: 最高频率值来填补缺失值的结果
- Analysis3.csv: 通过属性的相关关系来填补缺失值的结果
- Analysis4.csv: 通过数据对象之间的相似性来填补缺失值的结果
