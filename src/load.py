import pandas as pd
import psycopg2
from io import StringIO
from config.settings import settings
from src.logger import get_logger

class DataLoader:
   
   def __init__(self):
      self.logger = get_logger('load')
      
      self.conn = None
      
      self.cur = None
      
   def __enter__(self):
      self.conn = psycopg2.connect(settings.database_url)
      
      self.cur = self.conn.cursor()
      
      return self
   
   def __exit__(self, exc_type, exc_value, traceback):
      if exc_type is not None:
         self.conn.rollback()
         
         self.logger.error(f'Error occurred: {exc_value}')
         
      else:
         self.conn.commit()
         
         self.logger.info('Transaction committed successfully')
         
      self.cur.close()
      
      self.conn.close()
   
   def _create_staging_table(self, table_name, schema_sql):
      staging_name = f'{table_name}_staging'
      
      self.cur.execute(f'DROP TABLE IF EXISTS {staging_name} CASCADE;')
      
      self.cur.execute(f'CREATE TABLE {staging_name} ({schema_sql});')
      
      self.logger.info(f'Staging table {staging_name} created')
      
      return staging_name
   
   def _bulk_insert(self, df, table_name):
      buffer = StringIO()
      
      df.to_csv(buffer, index=False, header=False)
      
      buffer.seek(0)
      
      self.cur.copy_from(buffer, table_name, sep=',', columns=df.columns.tolist())
      
      self.logger.info(f'Loaded {table_name}')
      
   def _swap_tables(self, staging_name, final_name):
      backup = f'{final_name}_old'
      
      self.cur.execute('''
                       SELECT EXISTS (
                          SELECT FROM information_schema.tables
                          WHERE table_name = %s);''',
                        (final_name,)
                       )
      
      exists = self.cur.fetchone()[0]
      
      if exists:
         self.cur.execute(f'DROP TABLE IF EXISTS {backup};')
         
         self.cur.execute(f'ALTER TABLE {final_name} RENAME TO {backup};')
          
      self.cur.execute(f'ALTER TABLE {staging_name} RENAME TO {final_name};')
      
      if exists:
         self.cur.execute(f'DROP TABLE {backup};')
          
      self.logger.info(f'Swapped {staging_name} to {final_name}')
      
   def _add_indexes(self, table_name, indexes):
      for col in indexes:
         index_name = f'idx_{table_name}_{col}'
         
         self.cur.execute(f'CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({col});')
         
         self.logger.info(f'Created index: {index_name}')
         
   def load_agents(self, df):
      schema = '''
         agent_id INTEGER PRIMARY KEY,
         first_name TEXT,
         last_name TEXT,
         email TEXT,
         phone TEXT,
         license_number INTEGER,
         specialization TEXT,
         city TEXT,
         hire_date DATE,
         is_active BOOLEAN'''
      
      staging = self._create_staging_table('agents', schema)
      
      self._bulk_insert(df, staging)
      
      self._swap_tables(staging, 'agents')
      
      self._add_indexes('agents', ['city', 'specialization', 'is_active'])
      
   def load_clients(self, df):
      schema = '''
         client_id INTEGER PRIMARY KEY,
         first_name TEXT,
         last_name TEXT,
         email TEXT,
         phone TEXT,
         client_type TEXT,
         preferred_city TEXT,
         budget NUMERIC(12,2),
         signup_date DATE,
         is_active BOOLEAN'''
         
      staging = self._create_staging_table('clients', schema)
      
      self._bulk_insert(df, staging)
      
      self._swap_tables(staging, 'clients')
      
      self._add_indexes('clients', ['preferred_city', 'client_type'])
      
   def load_properties(self, df):
      schema = '''
         property_id INTEGER PRIMARY KEY,
         address TEXT,
         city TEXT,
         zip_code TEXT,
         property_type TEXT,
         listing_type TEXT,
         sqft INTEGER,
         price NUMERIC(12,2),
         year_built INTEGER,
         agent_id INTEGER REFERENCES agents(agent_id),
         listed_date DATE,
         is_available BOOLEAN'''
      
      staging = self._create_staging_table('properties', schema)
      
      self._bulk_insert(df, staging)
      
      self._swap_tables(staging, 'properties')
      
      self._add_indexes('properties', ['city', 'property_type', 'listing_type', 'agent_id'])
      
   def load_transactions(self, df):
      schema = '''
         transaction_id INTEGER PRIMARY KEY,
         property_id INTEGER REFERENCES properties(property_id),
         agent_id INTEGER REFERENCES agents(agent_id),
         client_id INTEGER REFERENCES clients(client_id),
         transaction_type TEXT,
         status TEXT,
         list_price NUMERIC(12,2),
         sale_price NUMERIC(12,2),
         commission_earned NUMERIC(12,2),
         close_date DATE'''
         
      staging = self._create_staging_table('transactions', schema)
      
      self._bulk_insert(df, staging)
      
      self._swap_tables(staging, 'transactions')
      
      self._add_indexes('transactions', ['property_id', 'agent_id', 'client_id', 'status', 'close_date'])
      
   def run_full_load(self, agents_df, clients_df, properties_df, transactions_df):
      self.logger.info('Starting full database load...')
      
      self.load_agents(agents_df)
      
      self.load_clients(clients_df)
      
      self.load_properties(properties_df)
      
      self.load_transactions(transactions_df)
      
      self.logger.info('Full load complete!!')
      