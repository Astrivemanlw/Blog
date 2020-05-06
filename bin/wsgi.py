from dotenv import load_dotenv
import os
from aweblog import create_app

path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path):
    load_dotenv(path)

app = create_app('production')
