import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as md
from mpl_finance import candlestick_ohlc
import yfinance as yf
from cryptocmd import CmcScraper
import statsmodels.api as sm
from itertools import product
import warnings
from datetime import datetime
import io 
import base64
import urllib



today = date.today()
date_x = today - timedelta(days=3650)
dates = pd.date_range(start= date_x, end = today ).strftime("%Y-%m-%d")
dates_list = dates.to_list()

plt.rcParams.update({
    "lines.color": "black",
    "patch.edgecolor": "black",
    "text.color": "black",
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


def getdata(sybmbol):
    scraper = CmcScraper(sybmbol, str(date_x.strftime('%d-%m-%Y')), str(today.strftime('%d-%m-%Y')))
    df = scraper.get_dataframe()
    df.reset_index(inplace=True)
    df['date'] = df['Date']
    df['Date'] = md.date2num(df['Date'].dt.date)

    return df

def getcandleChart(sybmbol):
    df = getdata(sybmbol)
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
    return plot_data

def prediction(sybmbol):
    raw_df = getdata(sybmbol)
    raw_df.index = raw_df.date
    raw_df.head()

    raw_df = raw_df.resample('D').mean()
    df_month = raw_df.resample('M').mean()
    Qs = range(0, 2)
    qs = range(0, 3)
    Ps = range(0, 3)
    ps = range(0, 3)
    D=1
    d=1
    parameters = product(ps, qs, Ps, Qs)
    parameters_list = list(parameters)
    len(parameters_list)

# Model Selection
    results = []
    best_aic = float("inf")
    warnings.filterwarnings('ignore')
    for param in parameters_list:
        try:
            model=sm.tsa.statespace.SARIMAX(df_month.Close, order=(param[0], d, param[1]), seasonal_order=(param[2], D, param[3], 12)).fit(disp=-1)
        except ValueError:
            print('wrong parameters:', param)
            continue
        aic = model.aic
    if aic < best_aic:
        best_model = model
        best_aic = aic
        best_param = param
    results.append([param, model.aic])
    df_month2 = df_month[['Close']]
    date_list = [datetime(2023, 4, 30), datetime(2023, 5, 31), datetime(2023, 6, 30), datetime(2023, 7, 31), 
                datetime(2023, 8, 31), datetime(2023, 9, 30),datetime(2023, 10, 31),datetime(2023, 11, 30),datetime(2023, 12, 31)]
    future = pd.DataFrame(index=date_list, columns= df_month.columns)
    df_month2 = pd.concat([df_month2, future])
    from scipy import stats
    df_month2['forecast'] = best_model.predict(start=100, end=130)
    df_month2.Close.plot()

    df_month2.forecast.plot(color='r', ls='--', label='Predicted Closed Price')
    plt.legend()
    plt.title('Crypto exchanges, by months')
    plt.ylabel('mean USD')
    plt.show()
    print(df_month2['forecast'][-10:])

prediction('BTC') 