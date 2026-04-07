import os
import sys

# Add the 'backend' directory to the python path so it can resolve imports like 'database'
backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.append(backend_dir)

from app import app
