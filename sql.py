import sqlite3
  
# Connecting to sqlite
conn = sqlite3.connect('crypto.db')
cursor = conn.cursor()
cursor.execute('''INSERT INTO crypto VALUES ( 2,'ETH', 'Ethereum')''')
cursor.execute('''INSERT INTO crypto VALUES ( 3,'USDT', 'Tether')''')
cursor.execute('''INSERT INTO crypto VALUES ( 4,'XRP', 'Ripple')''')
cursor.execute('''INSERT INTO crypto VALUES ( 5,'BNB', 'Binance')''')

conn.commit()
conn.close()