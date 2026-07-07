import pandas as pd
import psycopg2
from transform import clean_clients, clean_agents, clean_properties, clean_transactions

def load_data():
   agents = clean_agents()
   clients = clean_clients()
   properties = clean_properties(agents)
   transactions = clean_transactions(properties, agents, clients)
   
   conn = psycopg2.connect(dbname='real_estate', user='naga', host='localhost')
   cur = conn.cursor()
   
   cur.execute('DROP TABLE IF EXISTS agents CASCADE;')
   cur.execute('DROP TABLE IF EXISTS clients CASCADE;')
   cur.execute('DROP TABLE IF EXISTS properties CASCADE;')
   cur.execute('DROP TABLE IF EXISTS transactions CASCADE;')
   
   cur.execute('''
               CREATE TABLE agents (
                  agent_id INTEGER PRIMARY KEY,
                  first_name TEXT,
                  last_name TEXT,
                  email TEXT,
                  phone TEXT,
                  license_number INTEGER,
                  specialization TEXT,
                  city TEXT,
                  hire_date DATE,
                  is_active BOOLEAN
               )''')
   
   for _, row in agents.iterrows():
      cur.execute(
         'INSERT INTO agents VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
         tuple(row)
      )
      
   cur.execute('''
               CREATE TABLE clients (
                  client_id INTEGER PRIMARY KEY,
                  first_name TEXT,
                  last_name TEXT,
                  email TEXT,
                  phone TEXT,
                  client_type TEXT,
                  preferred_city TEXT,
                  budget FLOAT,
                  signup_date DATE,
                  is_active BOOLEAN
               )
               ''')
   
   for _, row in clients.iterrows():
      cur.execute(
         'INSERT INTO clients VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (client_id) DO NOTHING',
         tuple(row)
      )
      
   cur.execute('''
               CREATE TABLE properties (
                  property_id INTEGER PRIMARY KEY,
                  address TEXT,
                  city TEXT,
                  zip_code TEXT,
                  property_type TEXT,
                  listing_type TEXT,
                  sqft INTEGER,
                  price FLOAT,
                  year_built INTEGER,
                  agent_id INTEGER REFERENCES agents(agent_id),
                  listed_date DATE,
                  is_available BOOLEAN
               )
               ''')
   
   for _, row in properties.iterrows():
      cur.execute(
         'INSERT INTO properties VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
         tuple(row)
      )
      
   cur.execute('''
               CREATE TABLE transactions (
                  transaction_id INTEGER PRIMARY KEY,
                  property_id INTEGER REFERENCES properties(property_id),
                  agent_id INTEGER REFERENCES agents(agent_id),
                  client_id INTEGER REFERENCES clients(client_id),
                  transaction_type TEXT,
                  status TEXT,
                  list_price FLOAT,
                  sale_price FLOAT,
                  commission_earned FLOAT,
                  close_date DATE
               )
               ''')
   
   for _, row in transactions.iterrows():
      cur.execute(
         'INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
         tuple(row)
      )
      
   conn.commit()
   cur.close()
   conn.close()
   
if __name__ == '__main__':
   load_data()
   print('Data loaded!')
   