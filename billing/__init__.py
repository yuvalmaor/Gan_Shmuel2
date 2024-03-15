import logging

print("This file runs before the app")
print(f"__name__: {__name__}")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)