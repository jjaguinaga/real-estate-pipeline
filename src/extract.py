import pandas as pd 
from pathlib import Path 
from config.settings import settings
from src.logger import get_logger

class DataExtractor:
   
   def __init__(self, raw_path=None):
      self.raw_path = raw_path or settings.RAW_DATA_PATH
      
      self.logger = get_logger('extract')
         
   def _read_csv(self, filename: str):
      file_path = self.raw_path / filename
      
      self.logger.info(f'Reading {filename}')
      
      df = pd.read_csv(file_path, dtype=str, keep_default_na=True)
      
      self.logger.info(f'Loaded {len(df)} rows from {filename}')
      
      return df
   
   def extract_agents(self):
      return self._read_csv('raw_agents.csv')
   
   def extract_clients(self):
      return self._read_csv('raw_clients.csv')
   
   def extract_properties(self):
      return self._read_csv('raw_properties.csv')
   
   def extract_transactions(self):
      return self._read_csv('raw_transactions.csv')
