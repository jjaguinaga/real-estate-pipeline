from src.extract import DataExtractor
from src.transform import DataTransformer

# Extract all tables
extractor = DataExtractor()
raw_agents = extractor.extract_agents()
raw_clients = extractor.extract_clients()
raw_properties = extractor.extract_properties()
raw_transactions = extractor.extract_transactions()

# Transform in dependency order
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

# Summary
print("\n" + "="*50)
print("PIPELINE SUMMARY")
print("="*50)
print(f"Agents:       {len(clean_agents)} rows")
print(f"Clients:      {len(clean_clients)} rows")
print(f"Properties:   {len(clean_properties)} rows")
print(f"Transactions: {len(clean_transactions)} rows")
print("="*50)