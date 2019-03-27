# -*- coding: utf-8 -*-
"""3_Prediction_script_5_days

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1of4vmsyRdoBc3ilFZ9xgGxXn_jyuE6bI
"""

# Load the Drive helper and mount
# from google.colab import drive

# This will prompt for authorization.
# drive.mount('/content/drive')

# import os
   
# os.chdir('/content/drive/My Drive/drive1/SIH2019/ephemeris')
# os.getcwd()

import pandas as pd
import numpy as np
from fbprophet import Prophet
import glob
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go
import cmath
import os

days_to_predict = 1
periods =  24 * days_to_predict

df_final = pd.DataFrame()
# os.chdir('csv_files')
df_final = pd.DataFrame()
for file in glob.glob("csv_files/*.csv"):
  df = pd.read_csv(file)
  df_final = df_final.append(df, ignore_index=True)
os.chdir('..')

# df_final = df_final.append(pd.read_csv("csv_files/211011117.17N.csv"))
# df_final = df_final.append(pd.read_csv("csv_files/211021117.17N.csv"))
# df_final = df_final.append(pd.read_csv("csv_files/211031117.17N.csv"))
# df_final = df_final.append(pd.read_csv("csv_files/211041117.17N.csv"))
# df_final = df_final.append(pd.read_csv("csv_files/211051117.17N.csv"))

# df_expect = pd.read_csv("csv_files/211061117.17N.csv")

df_final['epoch_time']=pd.to_datetime(df_final['epoch_time'], format='%Y-%m-%d %H:%M:%S')
df_final = df_final.sort_values(by=['epoch_time'])

df_final.shape

df_prn = df_final.loc[df_final['prn'] == 3].reset_index()
df_prn.head()

df_prn.shape

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mapr = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    if mapr > 100:
      mapr = mapr%100
    return 0.0 if mapr!=mapr else mapr

df_predicted = pd.DataFrame()
avg_acc = 0.0

df2 = pd.DataFrame()
df2['ds'] = df_prn['epoch_time']
df2['y'] = df_prn['epoch_time']
model = Prophet()
model.fit(df2)
future = model.make_future_dataframe(periods=days_to_predict, freq='H')
forecast=model.predict(future)
df_predicted = future


for column in list(df_prn.columns.values):
  if column == 'prn' or column == 'epoch_time' or column=='index':
      continue
      
  if column == 'sv_clock_bias' or column == 'sv_clock_drift' or column == 'sv_clock_drift_rate' or column == 'mean_motion'  or  column == 'essentricity'  or column == 'sqrt_semi_major_axis'  or column == 'OMEGA' or column == 'inclination'  or column == 'omega' or column == 'OMEGA_dot' or column == 'inclination_rate' or column == 'codes' or column == 'gps_week' or column == 'l2_p_data_flag' or column == 'sv_accuracy' or column == 'sv_health' or column == 'tgd'  or column == 'fit_interval':
    df_m = pd.DataFrame()
    df_m['ds'] = df_prn['epoch_time']
    df_m['y'] = df_prn[column]

    model = Prophet()
    model.fit(df_m)

    future = model.make_future_dataframe(periods=days_to_predict, freq='H')
    forecast=model.predict(future)
    df_predicted[column] = forecast['yhat']
    path_img = 'img/'+column+'.png'
    model.plot(forecast).savefig('img/'+column+'.png')
    #model.plot(forecast)
    #print('RMSE: %f' % np.sqrt(np.mean((forecast.loc[:df_m['y'].size-1, 'yhat']-df_m['y'])**2)) )
    mse = mean_absolute_percentage_error(forecast.loc[:df_m['y'].size-1, 'yhat'],df_m['y'])
    #print("MSE: "+str(mse))
    avg_acc = avg_acc + mse
    del df_m

  if column == 'iode' or column == 'correction_radius_sine' or  column == 'correction_latitude_cosine' or column == 't_tx' or column == 'correction_latitude_sine' or  column == 'correction_inclination_cosine' or   column == 'correction_radius_cosine' or column == 'mean_anomaly' or  column == 'correction_inclination_sine':
    df_m = pd.DataFrame()
    df_m['ds'] = df_prn['epoch_time']
    df_m['y'] = df_prn[column]

    model = Prophet(changepoint_prior_scale=0.5)
    model.fit(df_m)

    future = model.make_future_dataframe(periods=days_to_predict, freq='H')
    forecast=model.predict(future)
    df_predicted[column] = forecast['yhat']
    path_img = 'img/'+column+'.png'
    model.plot(forecast).savefig(path_img)
    #model.plot(forecast)
    #print('RMSE: %f' % np.sqrt(np.mean((forecast.loc[:df_m['y'].size-1, 'yhat']-df_m['y'])**2)) )
    mse = mean_absolute_percentage_error(forecast.loc[:df_m['y'].size-1, 'yhat'],df_m['y'])
    #print("MSE: "+str(mse))
    avg_acc = avg_acc + mse    
    del df_m

  if column == 'time_of_ephemeris' or column == 'iodc' :
    df_m = pd.DataFrame()
    df_m['ds'] = df_prn['epoch_time']
    df_m['y'] = df_prn[column]

    model = Prophet(changepoint_prior_scale=1.0)
    model.fit(df_m)

    future = model.make_future_dataframe(periods=days_to_predict, freq='H')
    forecast=model.predict(future)
    df_predicted[column] = forecast['yhat']
    path_img = 'train_predict/img/'+column+'.png'
    model.plot(forecast).savefig('train_predict/img/'+column+'.png')
    #model.plot(forecast)
    #print('RMSE: %f' % np.sqrt(np.mean((forecast.loc[:df_m['y'].size-1, 'yhat']-df_m['y'])**2)) )
    mse = mean_absolute_percentage_error(forecast.loc[:df_m['y'].size-1, 'yhat'],df_m['y'])
    #print("MSE: "+str(mse))
    avg_acc = avg_acc + mse
    del df_m

    """    
      print('column  :'+ str(column))
      df2 = pd.DataFrame()
      df2['ds'] = df_prn_2['epoch_time']
      df2['y'] = df_prn_2[column]
      #print(df2.head())

      model = Prophet()
      model.fit(df2)

      future = model.make_future_dataframe(periods=30, freq='H')
      #print("future time")
      #print(future.tail(5))
      forecast=model.predict(future)
      df_predicted[column] = forecast['yhat']
      path_img = 'img/'+column+'.png'
      model.plot(forecast).savefig(path_img)

      print('RMSE: %f' % np.sqrt(np.mean((forecast.loc[:df2['y'].size-1, 'yhat']-df2['y'])**2)) )
      mse = mean_absolute_percentage_error(forecast.loc[:df2['y'].size-1, 'yhat'],df2['y'])

      avg_acc = avg_acc + mse
      print("MSE: "+str(mse))
      del df2 
    """

# df_predicted

# df_expect

# df_predicted.to_csv(r'predicted/predict_1.csv')

# avg_acc/30

# df_final.head(10)


