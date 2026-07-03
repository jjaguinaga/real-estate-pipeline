import pandas as pd

def get_agents():
   return pd.read_csv('raw-data/raw_agents.csv')

def clean_agents():
   df = get_agents()
   
   return df

def get_clients():
   return pd.read_csv('raw-data/raw_clients.csv')

def clean_clients():
   df = get_clients()
   
   return df

def get_properties():
   return pd.read_csv('raw-data/raw_properties.csv')

def clean_properties():
   df = get_properties()
   
   return df

def get_transactions():
   return pd.read_csv('raw-data/raw_transactions.csv')

def clean_transactions():
   df = get_transactions()
   
   return df

if __name__ == '__main__':
   agents_df = clean_agents()
   clients_df = clean_clients()
   properties_df = clean_properties()
   transactions_df = clean_transactions()
   pd.set_option('display.max_columns', None)
   pd.set_option('display.max_rows', None)
   print(agents_df.head())
   print(agents_df.info())
   print(clients_df.head())
   print(clients_df.info())
   print(properties_df.head())
   print(properties_df.info())
   print(transactions_df.head())
   print(transactions_df.info())
   
   