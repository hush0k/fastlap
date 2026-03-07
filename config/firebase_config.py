import firebase_admin
from firebase_admin import credentials, firestore
from decouple import config
from pathlib import Path

_app = None
_db = None

def get_firestore_client():
  """Get or create Firestore client singleton"""
  global _app, _db
    
  if _db is None:
    try:
      _app = firebase_admin.get_app()
    except ValueError:
      cred_path = Path(__file__).parent / 'firebase-credentials.json'
      cred = credentials.Certificate(str(cred_path))
            
      _app = firebase_admin.initialize_app(cred, {
        'projectId': config('FIREBASE_PROJECT_ID', 'fastlap-155b6'),
      })

    _db = firestore.client()
    
  return _db