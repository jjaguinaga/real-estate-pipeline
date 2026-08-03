import pandas as pd
import numpy as np
import re
from config.settings import settings
from src.logger import get_logger
from datetime import datetime

class DataTransformer:
   
   def __init__(self):
      self.logger = get_logger('transform')
      
      self.quarantine_dfs = []
      
      self._clear_quarantine()
      
   def _clear_quarantine(self):
      for file in settings.QUARANTINE_PATH.glob('quarantine_*.csv'):
         file.unlink()
      
      self.logger.info('Cleared old quarantine files')
     
   def _save_quarantine(self, df, name):
      timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
      
      if df.empty:
         return
      
      filename = settings.QUARANTINE_PATH / f'quarantine_{name}_{timestamp}.csv'
      
      df.to_csv(filename, index=False)
      
      self.logger.info(f'Quarantined {len(df)} rows to {filename}')
      
      self.quarantine_dfs.append(df)
      
   def _normalize_phone(self, phone):
      if phone is None or str(phone).lower() in ('none', 'nan', ''):
         return '800-000-0000'
      
      else:
         phone = re.sub(r'\D', '', str(phone))
         
         if len(phone) == 10:
            return f'{phone[:3]}-{phone[3:6]}-{phone[6:]}'
         
         elif len(phone) == 11 and phone.startswith('1'):
            return f'{phone[1:4]}-{phone[4:7]}-{phone[7:]}'
         
         else:
            self.logger.warning(f'Invalid phone format: {phone}')
            
            return f'INVALID:{phone}'
            
   def _parse_boolean(self, value):
      if pd.isna(value):
         return None
      
      else:
         mapping = {
            'true': True, '1': True, 'yes': True,
            'false': False, '0': False, 'no': False
         }
         
         result = mapping.get(str(value).lower().strip())
         
         if result is None:
            self.logger.warning(f'Invalid boolean value: {value}')
            
         return result 
      
   def transform_agents(self, df):
      self.logger.info('Transforming agents...')
      
      df = df.drop(columns=['commission_rate'], errors='ignore')
      
      bad_license = df['license_number'].isna()
      
      if bad_license.any():
         self._save_quarantine(df[bad_license], 'agents_null_license')
      
      df = df[~bad_license].copy()
      
      df['agent_id'] = pd.to_numeric(df['agent_id'], errors='coerce')
      
      bad_ids = df['agent_id'].isna()
      
      if bad_ids.any():
         self._save_quarantine(df[bad_ids], 'agents_bad_id')
      
      df = df[~bad_ids].copy()
      
      df['agent_id'] = df['agent_id'].astype(int)
         
      df['first_name'] = df['first_name'].str.strip().str.title()
      
      df['last_name'] = df['last_name'].str.strip().str.title()
      
      df['email'] = df['email'].fillna(df['first_name'].str[:1].str.lower() + df['last_name'].str.lower() + '@example.com').str.lower()
      
      df['phone'] = df['phone'].apply(self._normalize_phone)
      
      df['license_number'] = df['license_number'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(int)
      
      df['specialization'] = df['specialization'].str.lower()
         
      df['city'] = df['city'].str.title().replace({'Sf': 'San Francisco', 'La': 'Los Angeles'})
      
      df['hire_date'] = pd.to_datetime(df['hire_date'], format='mixed', errors='coerce')
      
      df['is_active'] = df['is_active'].apply(self._parse_boolean)
      
      before = len(df)
      
      df = df.drop_duplicates(subset=['agent_id'])
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} duplicate agent_ids')
      
      self.logger.info(f'Agents transformed: {len(df)} rows')
      
      return df 

   def transform_clients(self, df):
      self.logger.info(f'Transforming clients...')
      
      df['budget'] = df['budget'].replace(r'[^\d.]', '', regex=True).astype(float)
      
      bad_budget = df['budget'].isna()
      
      if bad_budget.any():
         self._save_quarantine(df[bad_budget], 'clients_null_budget')
         
      df = df[~bad_budget].copy()
      
      negative_budget = df['budget'] <= 0
      
      if negative_budget.any():
         self._save_quarantine(df[negative_budget], 'clients_invalid_budget')
         
      df = df[~negative_budget].copy()
      
      df['client_id'] = pd.to_numeric(df['client_id'], errors='coerce')
            
      bad_ids = df['client_id'].isna()
      
      if bad_ids.any():
         self._save_quarantine(df[bad_ids], 'clients_bad_id')
      
      df = df[~bad_ids].copy()
      
      df['client_id'] = df['client_id'].astype(int)
         
      df['first_name'] = df['first_name'].str.strip().str.title()
      
      df['last_name'] = df['last_name'].str.strip().str.title()
      
      df['email'] = df['email'].fillna(df['first_name'].str[:1].str.lower() + df['last_name'].str.lower() + '@example.com').str.lower()
      
      df['phone'] = df['phone'].apply(self._normalize_phone)
      
      df['client_type'] = df['client_type'].str.lower()
      
      df['preferred_city'] = df['preferred_city'].str.title().replace({'Sf': 'San Francisco', 'La': 'Los Angeles'})
      
      df['signup_date'] = pd.to_datetime(df['signup_date'], format='mixed', errors='coerce')
      
      df['is_active'] = df['is_active'].apply(self._parse_boolean)
      
      before = len(df)
      
      df = df.drop_duplicates(subset=['client_id'])
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} duplicate client_ids')
         
      self.logger.info(f'Clients transformed: {len(df)} rows')
      
      return df 
      
   def transform_properties(self, df, valid_agent_ids: set):
      self.logger.info(f'Transforming properties...')
      
      df['property_id'] = pd.to_numeric(df['property_id'], errors='coerce')
      
      bad_ids = df['property_id'].isna()
      
      if bad_ids.any():
         self._save_quarantine(df[bad_ids], 'properties_bad_id')
      
      df = df[~bad_ids].copy()
      
      df['agent_id'] = pd.to_numeric(df['agent_id'], errors='coerce')
      
      bad_agent_ids = df['agent_id'].isna()
      
      if bad_agent_ids.any():
         self._save_quarantine(df[bad_agent_ids], 'properties_bad_agent_id')
         
      df = df[~bad_agent_ids].copy()
      
      before = len(df)
      
      df = df[df['agent_id'].isin(valid_agent_ids)].copy()
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} orphan properties')
         
      df = df.drop(columns=['bedrooms', 'bathrooms'], errors='ignore')
      
      bad_address = df['address'].isna()
      
      if bad_address.any():
         self._save_quarantine(df[bad_address], 'properties_null_address')
         
      df = df[~bad_address].copy()
      
      bad_sqft = df['sqft'].isna()
      
      if bad_sqft.any():
         self._save_quarantine(df[bad_sqft], 'properties_null_sqft')
         
      df = df[~bad_sqft].copy()
      
      df['year_built'] = pd.to_numeric(df['year_built'], errors='coerce').fillna(0).astype(int)
      
      df['city'] = df['city'].str.title().replace({'Sf': 'San Francisco', 'La': 'Los Angeles'})
      
      df['property_type'] = df['property_type'].str.lower().replace({
         'condo': 'condominium', 
         'single-family': 'single family', 
         'town house': 'townhome', 
         'townhouse': 'townhome', 
         'multi-family': 'multi family'})
      
      df['sqft'] = df['sqft'].replace(r'[^\d]', '', regex=True).astype(int)
      
      df['listing_type'] = df['listing_type'].str.lower().replace({
         'for sale': 'sale', 
         'rental': 'rent', 
         'for rent': 'rent'})
      
      df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).astype(float)
      
      df['listed_date'] = pd.to_datetime(df['listed_date'], format='mixed', errors='coerce')
      
      df['is_available'] = df['is_available'].apply(self._parse_boolean)
      
      before = len(df)
      
      df = df.drop_duplicates(subset=['property_id'])
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} duplicate property_ids') 
         
      self.logger.info(f'Properties transformed: {len(df)} rows')
      
      return df 
   
   def transform_transactions(self, df, valid_property_ids: set, valid_agent_ids: set, valid_client_ids: set):
      self.logger.info(f'Transforming transactions...')
      
      df['transaction_id'] = pd.to_numeric(df['transaction_id'], errors='coerce')
      
      bad_ids = df['transaction_id'].isna()
      
      if bad_ids.any():
         self._save_quarantine(df[bad_ids], 'transactions_bad_id')
         
      df = df[~bad_ids].copy()
      
      df['property_id'] = pd.to_numeric(df['property_id'], errors='coerce')
      
      bad_pid = df['property_id'].isna()
      
      if bad_pid.any():
         self._save_quarantine(df[bad_pid], 'transactions_bad_property_id')
         
      df = df[~bad_pid].copy()
      
      before = len(df)
      
      df = df[df['property_id'].isin(valid_property_ids)].copy()
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} orphan transactions')
         
      df['agent_id'] = pd.to_numeric(df['agent_id'], errors='coerce')
      
      bad_aid = df['agent_id'].isna()
      
      if bad_aid.any():
         self._save_quarantine(df[bad_aid], 'transactions_bad_agent_id')
         
      df = df[~bad_aid].copy()
      
      before = len(df)
      
      df = df[df['agent_id'].isin(valid_agent_ids)].copy()
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} orphan transactions')
         
      df['client_id'] = pd.to_numeric(df['client_id'], errors='coerce')
      
      bad_cid = df['client_id'].isna()
      
      if bad_cid.any():
         self._save_quarantine(df[bad_cid], 'transactions_bad_client_id')
         
      df = df[~bad_cid].copy()
      
      before = len(df)
      
      df = df[df['client_id'].isin(valid_client_ids)].copy()
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} orphan transactions')
         
      df = df.drop(columns=['days_on_market'], errors='ignore')
      
      for col in ['list_price', 'sale_price', 'commission_earned']:
         df[col] = df[col].replace(r'[^\d.]', '', regex=True).astype(float)
         
      null_commission = df['commission_earned'].isna()
      
      if null_commission.any():
         self._save_quarantine(df[null_commission], 'transactions_null_commission')
         
      df = df[~null_commission].copy()
      
      null_sale = df['sale_price'].isna()
      
      if null_sale.any():
         self._save_quarantine(df[null_sale], 'transactions_null_sale')
         
      df = df[~null_sale].copy()
      
      null_list = df['list_price'].isna()
      
      if null_list.any():
         self._save_quarantine(df[null_list], 'transactions_null_list')
         
      df = df[~null_list].copy()
      
      before = len(df)
      
      negative_commission = df['commission_earned'] <= 0
      
      if negative_commission.any():
         self._save_quarantine(df[negative_commission], 'transactions_invalid_commission')
         
      df = df[~negative_commission].copy()
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} invalid commissions')
         
      before = len(df)
      
      excess_commission = df['commission_earned'] > df['sale_price']
      
      if excess_commission.any():
         self._save_quarantine(df[excess_commission], 'transactions_excess_commission')
         
      df = df[~excess_commission].copy()
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} excess commissions')
         
      df['transaction_type'] = df['transaction_type'].str.lower().replace({'lease': 'rental', 'purchase': 'sale'})
      
      df['status'] = df['status'].str.lower().replace({'close': 'closed', 'active': 'pending', 'canceled': 'cancelled', 'withdrawn': 'cancelled'})
      
      df['close_date'] = pd.to_datetime(df['close_date'], format='mixed', errors='coerce')
      
      before = len(df)
      
      df = df.drop_duplicates(subset=['transaction_id'])
      
      if len(df) < before:
         self.logger.warning(f'Removed {before - len(df)} duplicate transaction_ids')
         
      self.logger.info(f'Transactions transformed: {len(df)} rows')
         
      return df 
   