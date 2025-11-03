import os

# Path to input log file
LOG_PATH = "logs/dlpSite1.log"

# Number of lines per block sent to GPT
BLOCK_SIZE = 20

# Output folder for saving report files
OUTPUT_DIR = "output"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
