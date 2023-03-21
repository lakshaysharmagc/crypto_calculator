from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta

y1 = '2022'
M1 = 12 # Month count
begin2022 = pd.date_range(y1, periods=M1, freq='MS').strftime("%Y-%m-%d")
end2022 = pd.date_range(y1, periods=M1, freq='M').strftime("%Y-%m-%d")
begin2022 = begin2022.tolist()
end2022 = end2022.tolist()

# Dates for 2023
y2 = '2023'
M2 = 2 # Month count
begin2023 = pd.date_range(y2, periods=2, freq='MS').strftime("%Y-%m-%d")
end2023 = pd.date_range(y2, periods=M2, freq='M').strftime("%Y-%m-%d")
begin2023 = begin2023.tolist()
end2023 = end2023.tolist()

today = date.today()
# Yesterday date
yesterday = today - timedelta(days = 1)

yes_str = yesterday.strftime("%Y-%m-%d")
yes_lst = list(yes_str.split(" "))

#Combining both lists
start_date = begin2022 + begin2023
end_date = end2022 + end2023 

res = {start_date[i]: end_date[i] for i in range(len(start_date))}  

def getchart(symbol):
    lineChart=[]
    for start, end in res.items():
        url = "https://api.exchangerate.host/fluctuation?start_date=" + start + "&end_date=" +  end + "&symbols=" + symbol + '&base=USD' + "&format=json&source=crypto"
        r = requests.get(url)
        print(url)
        if r.status_code == 200:
            data = r.json()
            d = data["rates"][symbol]["change_pct"]
            lineChart.append(d)
        else:
            exit()
    return lineChart