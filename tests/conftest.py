"""
Configuration pytest pour ajouter le projet au PYTHONPATH
"""

import sys
import os

# Ajouter la racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))