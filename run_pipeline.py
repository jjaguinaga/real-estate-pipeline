from src.extract import DataExtractor
from src.transform import DataTransformer
from src.load import DataLoader
from src.logger import get_logger

def main():
   extractor = DataExtractor()
   
   raw_agents = extractor.extract_agents()
   
   raw_clients = extractor.extract_clients()
   
   raw_properties = extractor.extract_properties()
   
   raw_transactions = extractor.extract_transactions()
   
   transformer = DataTransformer()

   clean_agents = transformer.transform_agents(raw_agents)
   valid_agent_ids = set(clean_agents['agent_id'])

   clean_clients = transformer.transform_clients(raw_clients)
   valid_client_ids = set(clean_clients['client_id'])

   clean_properties = transformer.transform_properties(raw_properties, valid_agent_ids)
   valid_property_ids = set(clean_properties['property_id'])

   clean_transactions = transformer.transform_transactions(
      raw_transactions, 
      valid_property_ids, 
      valid_agent_ids, 
      valid_client_ids
   )
   
   with DataLoader() as loader:
      loader.run_full_load(
         clean_agents,
         clean_clients,
         clean_properties,
         clean_transactions
      )
   
   logger = get_logger('pipeline')
   
   logger.info(f'agents: {len(clean_agents)} rows. clients: {len(clean_clients)} rows. properties: {len(clean_properties)} rows. transactions: {len(clean_transactions)} rows')
   
if __name__ == '__main__':
   main()
   