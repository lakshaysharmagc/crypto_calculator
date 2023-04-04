from flask import Flask, jsonify, request, render_template
import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta

today = date.today()
date_x = today - timedelta(days=365)
dates = pd.date_range(start= date_x, end = today ).strftime("%Y-%m-%d")
dates_list = dates.to_list()


def getHistoricData(symbol):
    start_rates= []
    end_rates= []
    date = []

    for i in range(len(dates_list)-1):
        
        url = "https://api.exchangerate.host/fluctuation?start_date=" + dates_list[i] + "&end_date=" +  dates_list[i+1] + "&symbols=" + symbol + '&base=USD' + "&format=json&source=crypto"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            start = data["rates"][symbol]["start_rate"]
            end = data["rates"][symbol]["end_rate"]
            date.append(dates_list[i])
            start_rates.append(start)
            end_rates.append(end)
        data = pd.DataFrame(date)
        data['start_rates'] = start_rates
        data['end_rates'] = end_rates

        print(data)

getHistoricData('XRP')
