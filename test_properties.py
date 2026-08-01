from src.extract import DataExtractor
from src.transform import DataTransformer

# Extract
extractor = DataExtractor()
raw_agents = extractor.extract_agents()
raw_properties = extractor.extract_properties()

# Transform agents first (needed for valid IDs)
transformer = DataTransformer()
clean_agents = transformer.transform_agents(raw_agents)

# Get valid agent IDs
valid_agent_ids = set(clean_agents['agent_id'])
print(f"Valid agent IDs: {len(valid_agent_ids)}")

# Transform properties
clean_properties = transformer.transform_properties(raw_properties, valid_agent_ids)

print(f"\nClean properties: {len(clean_properties)} rows")
print(clean_properties.head(3))
print(f"\nClean dtypes:\n{clean_properties.dtypes}")