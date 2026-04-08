import sys
import os
from flask import Flask

backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.append(backend_dir)

# Initialize Flask app explicitly for Vercel AST builder
app = Flask(__name__)

# Replace it with our backend app immediately at runtime
import backend.app as backend_app
app = backend_app.app
