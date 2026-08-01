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
   df['license_number'] = df['license_number'].astype(int)
   df['specialization'] = df['specialization'].str.lower()
   df['city'] = df['city'].str.title().replace({'Sf': 'San Francisco', 'La': 'Los Angeles'})
   df['hire_date'] = pd.to_datetime(df['hire_date'], format='mixed')
   df['is_active'] = df['is_active'].str.lower().map({'true': True, 'false': False, '1': True, '0': False, 'yes': True, 'no': False})
   df = df.drop_duplicates()
   return df

def get_clients():
   return pd.read_csv('raw-data/raw_clients.csv')

def clean_clients():
   df = get_clients()
   df = df.dropna(subset=['budget'])
   df['first_name'] = df['first_name'].str.capitalize()
   df['last_name'] = df['last_name'].str.capitalize()
   df[['email', 'phone']] = df[['email', 'phone']].fillna('None')
   df['phone'] = df['phone'].str.replace(r'(?:\+?1\D*)?\D*(\d{3})\D*(\d{3})\D*(\d{4})', r'\1-\2-\3', regex=True)
   df['client_type'] = df['client_type'].str.lower()
   df['preferred_city'] = df['preferred_city'].str.title().replace({'Sf': 'San Francisco', 'La': 'Los Angeles'})
   df['budget'] = df['budget'].replace(r'[^\d]', '', regex=True).astype(float)
   df['signup_date'] = pd.to_datetime(df['signup_date'], format='mixed')
   df['is_active'] = df['is_active'].str.lower().map({'true': True, 'false': False, '1': True, '0': False, 'yes': True, 'no': False})
   return df

def get_properties():
   return pd.read_csv('raw-data/raw_properties.csv')

def clean_properties(agents_df):
   df = get_properties()
   df = df[df['agent_id'].isin(agents_df['agent_id'])]
   df = df.drop(columns=['bedrooms', 'bathrooms'])
   df = df.dropna(subset=['address', 'sqft'])
   df['year_built'] = df['year_built'].fillna(0).astype(int)
   df['city'] = df['city'].str.title().replace({'Sf': 'San Francisco', 'La': 'Los Angeles'})
   df['property_type'] = df['property_type'].str.lower().replace({'condo': 'condominium', 'single-family': 'single family', 'town house': 'townhome', 'townhouse': 'townhome', 'multi-family': 'multi family'})
   df['sqft'] = df['sqft'].replace(r'[^\d]', '', regex=True).astype(int)
   df['listing_type'] =df['listing_type'].str.lower().replace({'for sale': 'sale', 'rental': 'rent', 'for rent': 'rent'})
   df['price'] = df['price'].replace(r'[\$]?\,?', '', regex=True).astype(float)
   df['listed_date'] = pd.to_datetime(df['listed_date'], format='mixed')
   df['is_available'] = df['is_available'].map({'true': True, 'false': False, 'True': True, 'False': False, '1': True, '0': False})
   return df

def get_transactions():
   return pd.read_csv('raw-data/raw_transactions.csv')

def clean_transactions(properties_df, agents_df, clients_df):
   df = get_transactions()
   df = df[df['property_id'].isin(properties_df['property_id'])]
   df = df[df['agent_id'].isin(agents_df['agent_id'])]
   df = df[df['client_id'].isin(clients_df['client_id'])]
   df = df.drop(columns=['days_on_market'])
   df = df.dropna(subset=['commission_earned'])
   df['transaction_type'] = df['transaction_type'].str.lower().replace({'lease': 'rental', 'purchase': 'sale'})
   df['status'] = df['status'].str.lower().replace({'close': 'closed', 'active': 'pending', 'canceled': 'cancelled', 'withdrawn': 'cancelled'})
   df[['list_price', 'sale_price', 'commission_earned']] = df[['list_price', 'sale_price', 'commission_earned']].replace(r'[\$]?\,?', '', regex=True).astype(float)
   df['commission_earned'] = df['commission_earned'].replace(r'\-', '', regex=True)
   df['close_date'] = pd.to_datetime(df['close_date'], format='mixed')  
   return df

if __name__ == '__main__':
    agents_df = clean_agents()
    clients_df = clean_clients()
    properties_df = clean_properties(agents_df)
    transactions_df = clean_transactions(properties_df, agents_df, clients_df)

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
   