from src.extract import DataExtractor
from src.transform import DataTransformer

# Extract
extractor = DataExtractor()
raw_clients = extractor.extract_clients()

print("RAW CLIENTS:")
print(raw_clients.head(3))
print(f"\nRaw dtypes:\n{raw_clients.dtypes}")

# Transform
transformer = DataTransformer()
clean_clients = transformer.transform_clients(raw_clients)

print("\nCLEAN CLIENTS:")
print(clean_clients.head(3))
print(f"\nClean dtypes:\n{clean_clients.dtypes}")