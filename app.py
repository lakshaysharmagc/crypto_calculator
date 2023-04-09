from flask import Flask ,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from recommend import *
import getdata as gs 
import recommend as rcd
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto.db'
server = app.server
db = SQLAlchemy(app)

def calculate(predicted_value,current,vol):
        messages ={}
        predicted_value = float(predicted_value)
        current = float(current)
        if(predicted_value > current ):
             gain = predicted_value - current
             gain_percent = ( (gain)/ current) *100
             gain_percent=(round(gain_percent, 2))
             messages['text'] = "You will able to gain with percent of {0} %".format(gain_percent)
             messages['sign'] = 'profit'
             messages['percent'] = gain_percent
             messages['text2'] = "You will able to gain a total of {0} USD by investing {1} coin right now ".format(round(gain*vol,2),2)
             messages['color'] = '#7ed957'
        else :
             loss= current - predicted_value
             loss_percent = ( ( loss )/ current) *100
             loss_percent=(round(loss_percent, 2))
             messages['text'] = "You will able to lost with percent of {0} %".format(loss_percent)
             messages['sign'] = 'loss'
             messages['percent'] = loss_percent  
             messages['text2'] = "You will loose a total of {0} USD by investing {1} coin(s) right now ".format( round(loss*vol,2) ,vol)
             messages['color'] = '#ff5757'
        return messages


class Crypto (db.Model):
        sno = db.Column(db.Integer,primary_key=True)
        symbol=db.Column(db.String(200),nullable=False)
        title = db.Column(db.String(200),nullable=False)
        def __repr__(self) -> str:
             return f"{self.symbol} -{self.title}"

@app.route('/home' ,methods =['GET','POST'])
def index():
    coins = Crypto.query.all()
    return render_template('index.html',coins = coins)
    
@app.route('/recommend/<coin>')
def recommend(coin):
    values = gs.getchart(coin)
    plot_data=rcd.getcandleChart(coin)
    Title = db.session.execute(db.select(Crypto.title).filter_by(symbol=coin)).scalar()
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'23","Feb'23"]
    return render_template('recommend.html',labels = months, values = values,coin =coin, plot_url=plot_data ,title = Title)



@app.route('/Calculator',methods =['GET','POST'])
def calculator():
    coins = Crypto.query.all()
    
    if request.method =="POST":
         coin=request.form['coin']
         actiontype=request.form['action_type']
         if actiontype == "coinonly":
            months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'23","Feb'23"]
            cv = gs.CurrentValue(coin)
            values = gs.getchart(coin)
            return render_template('calculator.html',current = cv ,coins = coins,labels = months ,values = values ,coin =coin,visibility="hidden")
         else:
            coin=request.form['coin']
            prediction = rcd.prediction(coin)
            term = request.form['Term']
            vol = request.form['vol']
            cv = gs.CurrentValue(coin)
            if(term == 'Short') :
                messages=calculate(prediction['3mon'],cv,int(vol))
                price = round(prediction['3mon'],4)
            else:
                messages=calculate(prediction['6mon'],cv,int(vol))
                price = round(prediction['6mon'],4)
            prediction_img = prediction['plot_data']
            results = prediction['result']

            mess = "Based on prediction of prices , Here are the Recommendation:"
            return render_template('calculator.html',term=term,visibility2="hidden" ,visibility="visible" ,price =price, current = cv ,mess = mess ,coins = coins ,coin =coin ,result = results , 
                                   text = messages['text'],text1 = messages['text2'],sign = messages['sign'],percent = messages['percent'] ,color = messages['color'] ,plot_url=prediction_img)
    else:
        return render_template('calculator.html',coins = coins,visibility="hidden" ,visibility2="visible")
@app.route('/Compare',methods =['GET','POST'])
def compare():
    coins = Crypto.query.all()
    if request.method =="POST":
         coin1=request.form['coin1']
         coin2=request.form['coin2']
         months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'23","Feb'23"]
         values1 = gs.getchart(coin1)
         values2 = gs.getchart(coin2)
         return render_template('comparrision.html',coins = coins,labels = months,values1  = values1 ,values2=values2,coin1 =coin1,coin2=coin2 )
    else:
         return render_template('comparrision.html',coins = coins)

if __name__ == "__main__":
    app.run(debug = True,port=4040)




