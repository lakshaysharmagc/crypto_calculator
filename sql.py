import sqlite3
  
# Connecting to sqlite
conn = sqlite3.connect('crypto.db')
cursor = conn.cursor()

#cursor.execute('''INSERT INTO crypto VALUES ( 2,'ETH', 'Ethereum')''')
cursor.execute('''INSERT INTO crypto VALUES ( 2,'ADA', 'Cardano')''')
#cursor.execute('''INSERT INTO crypto VALUES ( 4,'XRP', 'Ripple')''')
#cursor.execute('''INSERT INTO crypto VALUES ( 5,'BNB', 'Binance')''')
#cursor.execute('''Delete from crypto as c where c.symbol = 'USDT' ''')

conn.commit()
conn.close()