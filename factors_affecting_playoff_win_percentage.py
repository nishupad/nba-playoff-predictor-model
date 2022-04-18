# -*- coding: utf-8 -*-
"""Factors Affecting Playoff Win Percentage

Automatically generated by Colaboratory.

"""

# Commented out IPython magic to ensure Python compatibility.
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestClassifier
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBClassifier
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.datasets import make_regression
from numpy import loadtxt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# %matplotlib inline
plt.style.use('seaborn')
import requests
import re
import time
import statsmodels.api as sm
import scipy.stats as stats
import scipy as sp
import sklearn
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

"""Reading the Datasets from Basketball Reference below, and then merging them into one dataset. The data for playoff wins and playoff win percentage for each team was added manually by Aadrij Upadya."""

df_2021 = pd.read_csv("/content/2020-2021 - Sheet1.csv")
df_2020 = pd.read_csv("/content/2019-2020 - Sheet1.csv")
df_2019 = pd.read_csv("/content/2018-2019 - Sheet1.csv")
df_2018 = pd.read_csv("/content/2017-2018 - Sheet1.csv")
df_2017 = pd.read_csv("/content/2016-2017 - Sheet1.csv")
df_2016 = pd.read_csv("/content/2015-2016 - Sheet1.csv")
df_2015 = pd.read_csv("/content/2014-2015 - Sheet1.csv")

df_2021['Year'] = [2021 for x in range(len(df_2021.index))]
df_2020['Year'] = [2020 for x in range(len(df_2020.index))]
df_2019['Year'] = [2019 for x in range(len(df_2019.index))]
df_2018['Year'] = [2018 for x in range(len(df_2018.index))]
df_2017['Year'] = [2017 for x in range(len(df_2017.index))]
df_2016['Year'] = [2016 for x in range(len(df_2016.index))]
df_2015['Year'] = [2015 for x in range(len(df_2015.index))]

frames = [df_2021, df_2020, df_2019, df_2018, df_2017, df_2016, df_2015]
metadata = pd.concat(frames)

metadata = metadata.drop(columns=['Unnamed: 17', 'Unnamed: 22', 'Unnamed: 27', 'Unnamed: 21'])
metadata['Index'] = [x for x in range(len(metadata.index))]
metadata = metadata.set_index('Index')

cnt = 0
for team in metadata['Team']:
    if '*' not in str(team):
        metadata = metadata.drop(cnt)
    cnt+=1

metadata['Index'] = [x for x in range(len(metadata.index))]
metadata = metadata.set_index('Index')

from IPython.display import display
with pd.option_context('display.max_rows', 250):
    display(metadata)

metadata['Playoff Wins'] = [6,10,14,16,7,4,7,2,3,1,10,2,1,1,0,1,5,10,7,7,16,2,14,5,3,0,9,0,3,0,1,1,10,14,16,1,6,5,8,7,0,1,7,3,2,1,1,0,11,4,16,5,5,11,2,1,0,1,3,5,12,2,1,3,16,8,6,4,3,4,13,9,7,1,2,2,0,2,0,2,6,15,11,16,10,2,4,2,3,7,3,5,0,1,1,0,16,7,3,8,14,1,9,6,0,6,1,0,6,2,0,2]
metadata['Playoff Win Percentage'] = [0.545,0.526,0.636,0.696,0.583,0.400,0.583,0.333,0.429,0.200,0.556,0.333,0.200,0.200,0,0.200,0.500,0.588,0.538,0.636,0.762,0.333,0.667,0.417,0.429,0,0.474,0,0.429,0,0.200,0.200,0.667,0.636,0.667,0.200,0.545,0.556,0.500,0.500,0,0.200,0.583,0.429,0.333,0.200,0.200,0,0.647,0.400,0.762,0.455,0.500,0.579,0.333,0.200,0,0.200,0.429,0.556,0.545,0.333,0.200,0.429,0.941,0.500,0.545,0.400,0.429,0.364,0.722,0.500,0.538,0.200,0.333,0.333,0,0.333,0,0.333,0.600,0.625,0.611,0.762,0.500,0.333,0.400,0.333,0.429,0.500,0.429,0.455,0,0.200,0.200,0,0.762,0.500,0.429,0.500,0.700,0.200,0.529,0.545,0,0.500,0.200,0,0.600,0.333,0,0.33]

non_str_data = metadata.drop(columns=['Team','Arena','Year','Attend.'])
metadata.to_csv('metadata.csv')
np.set_printoptions(suppress=True)

non_str_data.to_csv('non_str_data.csv')

dataset = pd.read_csv('/content/non_str_data.csv')

"""The advanced statistics will be used to predict playoff win percentage using the XGBoost Regressor."""

X = dataset.iloc[:,1:26]
Y = dataset.iloc[:,27:28]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=40)

model = XGBRegressor(subsample=0.6, n_estimators=500, max_depth=3, learning_rate=0.01, colsample_bytree=0.7, colsample_bylevel=0.6)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

r2_score(y_pred, y_test)

predictions = [round(value,2) for value in y_pred]
print(predictions)
print(mean_squared_error(y_test,predictions))

fig, ax = plt.subplots(figsize=(12,8))
sns.heatmap(metadata.corr(), ax=ax, cmap='YlGnBu')
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)

"""Below, we can see which statistics are correlated with playoff win percentage."""

corr = metadata.corr()
abs(corr).sort_values(by = 'Playoff Win Percentage', ascending = False)['Playoff Win Percentage']

"""The correlation between different stats are visible using a scatter matrix."""

pd.plotting.scatter_matrix(X, figsize=(40,30))
plt.show()
