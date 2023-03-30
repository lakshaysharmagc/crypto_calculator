from flask import Flask ,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from recommend import *
import getdata as gs 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto.db'
db = SQLAlchemy(app)
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
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'23","Feb'23"]
    return render_template('recommend.html',labels = months, values = values,coin =coin )



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
            return render_template('calculator.html',current = cv ,coins = coins,labels = months ,values = values ,coin =coin)
         else:
            return render_template('calculator.html',current = cv ,coins = coins ,title= title )
    else:
        return render_template('calculator.html',coins = coins )
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




