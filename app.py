from flask import Flask ,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto.db'
db = SQLAlchemy(app)
class Crypto (db.Model):
        sno = db.Column(db.Integer,primary_key=True)
        symbol=db.Column(db.String(200),nullable=False)
        title = db.Column(db.String(200),nullable=False)

        def __repr__(self) -> str:
             return f"{self.symbol} -{self.title}"

@app.route('/' ,methods =['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/CyptoCalculator')
def calculator():
    return 'Cypto Calculator'
@app.route('/Compare',methods =['GET','POST'])
def compare():
    if request.method =="POST":
         print('Post')
    
    coins = Crypto.query.all()
    return render_template('compare.html',coins = coins)

if __name__ == "__main__":
    app.run(debug = True,port=4040)




