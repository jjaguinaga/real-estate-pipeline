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
      
   