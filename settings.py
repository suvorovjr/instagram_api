import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env')

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')