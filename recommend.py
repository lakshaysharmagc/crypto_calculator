import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md

from mpl_finance import candlestick_ohlc
from cryptocmd import CmcScraper
import statsmodels.api as sm
from itertools import product
import warnings
from datetime import datetime
import io 
import base64
import urllib
from scipy import stats




today = date.today()


plt.rcParams.update({
    "lines.color": "black",
    "patch.edgecolor": "black",
    "text.color": "lightgray",
    "axes.facecolor": "black",
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",
    "xtick.color": "lightgray",
    "ytick.color": "lightgray",
    "grid.color": "lightgray",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"})


def getdata(sybmbol,date_x):
    scraper = CmcScraper(sybmbol, str(date_x.strftime('%d-%m-%Y')), str(today.strftime('%d-%m-%Y')))
    df = scraper.get_dataframe()
    df.reset_index(inplace=True)
    df['date'] = df['Date']
    df['Date'] = md.date2num(df['Date'].dt.date)

    return df

def forecast_accuracy(forecast, actual):

    
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    str= "The accuracy of the model is {0}%".format( round(float(corr), 2)*100 )
    return str


def getcandleChart(sybmbol):
    date_x = today - timedelta(days=45)
    df = getdata(sybmbol,date_x)
    filtered_df = df[['Date','Open','High','Low','Close']]

    f,ax=plt.subplots(figsize=(10,5))
    ax.xaxis_date()

    candlestick_ohlc(ax, filtered_df.values, width=0.4, colorup='g', colordown='r',alpha=0.5)
     
    plt.xlabel("Date")
    ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    plt.title(" price")
    plt.ylabel("Price")
    img=io.BytesIO()
    plt.savefig( img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    plt.close()
    return plot_data

def prediction(sybmbol):
    data ={}
    date_x = today - timedelta(days=3650)
    raw_df = getdata(sybmbol,date_x)
    raw_df.index = raw_df.date
    raw_df.head()

    raw_df = raw_df.resample('D').mean()
    df_month = raw_df.resample('M').mean()
    Qs = range(0, 2)
    qs = range(0, 3)
    Ps = range(0, 3)
    ps = range(0, 3)
    D=1
    d=1 # after checking transformations
    parameters = product(ps, qs, Ps, Qs)
    parameters_list = list(parameters)
    len(parameters_list)

    results = []
    best_aic = float("inf")
    warnings.filterwarnings('ignore')
    for param in parameters_list:
        try:
            model=sm.tsa.statespace.SARIMAX(df_month.Close, order=(param[0], d, param[1]),seasonal_order=(param[2], D, param[3], 12)).fit(disp=-1)
        except ValueError:
            print('wrong parameters:', param)
            continue
        aic = model.aic
    if aic < best_aic:
        best_model = model
        best_aic = aic
    results.append([param, model.aic])
    df_month2 = df_month[['Close']]
    date_list = [ datetime(2023, 5, 31), datetime(2023, 6, 30), datetime(2023, 7, 31), 
             datetime(2023, 8, 31), datetime(2023, 9, 30),datetime(2023, 10, 31),datetime(2023, 11, 30),datetime(2023, 12, 31),datetime(2024, 1, 31)]
    future = pd.DataFrame(index=date_list, columns= df_month.columns)
    df_month2 = pd.concat([df_month2, future])
    df_month2['forecast'] = best_model.predict(start=0, end=150)
    df_month2['forecast'] = df_month2['forecast'].shift(-1) 
    df_month2.Close.plot()
    df_month2.forecast.plot(color='r', ls='--', label='Predicted Closed Price')
    plt.legend()
    plt.title('Crypto exchanges Prediction')
    plt.ylabel('mean USD')
    img=io.BytesIO()
    plt.savefig( img, format='png',dpi=125)
    img.seek(0)
    plt.close()
    data['plot_data'] = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    data['result'] =forecast_accuracy(df_month2.forecast[90:110],df_month2.Close[90:110])

    months_3 = today + timedelta(90)
    months_6 = today + timedelta(180)
    ind = df_month2.index.get_loc(str(months_3),method ='nearest')
    data['3mon'] = df_month2.forecast[ind]
    data['6mon'] = df_month2.forecast[df_month2.index.get_loc(str(months_6),method ='nearest')]
    return data





