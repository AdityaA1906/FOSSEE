import os
import sys

# Add the current directory to sys.path to allow imports from config and core
sys.path.append(os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from config.wsgi import application
app = application
