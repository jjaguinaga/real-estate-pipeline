from src.extract import DataExtractor

extractor = DataExtractor()

# Test agents
agents = extractor.extract_agents()
print(f"Agents shape: {agents.shape}")
print(agents.head(2))
print(f"Agent column types:\n{agents.dtypes}\n")

# Test clients
clients = extractor.extract_clients()
print(f"Clients shape: {clients.shape}")

# Test properties
properties = extractor.extract_properties()
print(f"Properties shape: {properties.shape}")

# Test transactions
transactions = extractor.extract_transactions()
print(f"Transactions shape: {transactions.shape}")
