from src.logger import get_logger

# Call twice with same name
logger1 = get_logger("transform")
logger2 = get_logger("transform")

# Call once with different name
logger3 = get_logger("load")

# Log from all three
logger1.info("Transform started")
logger2.info("Transform step 2")  # Should NOT create duplicate handlers
logger3.info("Load started")

print("Check logs/pipeline.log — how many lines?")
