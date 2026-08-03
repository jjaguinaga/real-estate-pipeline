import pandas as pd 
from src.transform import DataTransformer
import pytest

def test_normalize_phone_10_digits():
   transformer = DataTransformer()
   
   result = transformer._normalize_phone('1234567890')
   
   assert result == '123-456-7890'
   
@pytest.mark.parametrize('input_value,expected', [
   ('true', True),
   ('True', True),
   ('1', True),
   ('yes', True),
   ('false', False),
   ('0', False),
   ('no', False),
   (None, None),
   ('maybe', None)
])

def test_parse_boolean(input_value, expected):
   transformer = DataTransformer()
   
   result = transformer._parse_boolean(input_value)
   
   assert result == expected
   
def test_normalize_phone_invalid():
   transformer = DataTransformer()
   
   result = transformer._normalize_phone('123')
   
   assert result == 'INVALID:123'
   
def test_transform_agents_quarantines_null_license():
   raw = pd.DataFrame({
      'agent_id': ['1', '2'],
      'first_name': ['LAUREN', 'Kimberly'],
      'last_name': ['Nguyen', 'Ferguson'],
      'email': ['lauren@example.com', 'kim@example.com'],
      'phone': ['123-456-7890', '123-456-7899'],
      'license_number': ['12345', None],
      'specialization': ['residential', 'commercial'],
      'city': ['sf', 'la'],
      'hire_date': ['2020-01-01', '2021-06-15'],
      'is_active': ['true', 'false']
   })
   
   transformer = DataTransformer()
   
   clean = transformer.transform_agents(raw)
   
   assert len(transformer.quarantine_dfs) == 1
   assert len(transformer.quarantine_dfs[0]) == 1
   assert len(clean) == 1
   assert clean['agent_id'].iloc[0] == 1
   assert clean['first_name'].iloc[0] == 'Lauren'
   assert clean['city'].iloc[0] == 'San Francisco'
   assert clean['is_active'].iloc[0] == True
   
def test_transform_agents_remove_duplicates(caplog):
   raw = pd.DataFrame({
      'agent_id': ['1', '1'],
      'first_name': ['Juan', 'Juan'],
      'last_name': ['Naga', 'Naga'],
      'email': ['naga@example.com', 'naga@example.com'],
      'phone': ['123-456-7890', '123-456-7890'],
      'license_number': ['12345', '12345'],
      'specialization': ['residential', 'residential'],
      'city': ['San Francisco', 'San Francisco'],
      'hire_date': ['2020-01-01', '2020-01-01'],
      'is_active': [True, True]
   })
   
   transformer = DataTransformer()
   
   clean = transformer.transform_agents(raw)
   
   assert len(clean) == 1
   assert 'Removed 1 duplicate agent_ids' in caplog.text
   
   