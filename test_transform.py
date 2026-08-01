from src.extract import DataExtractor
from src.transform import DataTransformer

# Extract
extractor = DataExtractor()
raw_agents = extractor.extract_agents()

print("RAW DATA:")
print(raw_agents.head(3))
print(f"\nRaw dtypes:\n{raw_agents.dtypes}")

# Transform
transformer = DataTransformer()
clean_agents = transformer.transform_agents(raw_agents)

print("\nCLEAN DATA:")
print(clean_agents.head(3))
print(f"\nClean dtypes:\n{clean_agents.dtypes}")