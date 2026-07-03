import pandas as pd

def get_agents():
   return pd.read_csv('raw-data/raw_agents.csv')

def clean_agents():
   df = get_agents()
   df = df.drop(columns=['commission_rate'])
   df = df.dropna(subset=['license_number'])
   df['phone'] = df['phone'].fillna('800-000-0000')
   df['email'] = df['email'].fillna(df['first_name'].str[:1].str.lower() + df['last_name'].str.lower() + '@example.com')
   df['first_name'] = df['first_name'].str.capitalize()
   df['last_name'] = df['last_name'].str.capitalize()
   df['phone'] = df['phone'].str.replace(r'(?:\+?1\D*)?\D*(\d{3})\D*(\d{3})\D*(\d{4})', r'\1-\2-\3', regex=True)
   df['license_number'] = df['license_number'].str.replace(r'[^\d]', '', regex=True)
   df['specialization'] = df['specialization'].str.lower()
   df['city'] = df['city'].str.title().replace({'Sf': 'San Fransisco', 'La': 'Los Angeles'})
   df['hire_date'] = pd.to_datetime(df['hire_date'], format='mixed')
   df['is_active'] = df['is_active'].str.lower().replace({'true': True, 'false': False, '1': True, '0': False, 'yes': True, 'no': False})
   # df = df.drop_duplicates()
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
   # agents_df = clean_agents()
   clients_df = clean_clients()
   # properties_df = clean_properties()
   # transactions_df = clean_transactions()
   pd.set_option('display.max_columns', None)
   pd.set_option('display.max_rows', None)
   # print(agents_df.head())
   # print(agents_df.info())
   print(clients_df.head())
   print(clients_df.info())
   # print(properties_df.head())
   # print(properties_df.info())
   # print(transactions_df.head())
   # print(transactions_df.info())
   
   