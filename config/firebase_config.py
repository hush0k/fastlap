import firebase_admin
from decouple import config
from firebase_admin import credentials, firestore

from config.settings.base import FIREBASE_CREDENTIALS_PATH

_app = None
_db = None


def get_firestore_client():
    """Get or create Firestore client singleton"""
    global _app, _db

    if _db is None:
        try:
            _app = firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)

            _app = firebase_admin.initialize_app(
                cred,
                {
                    "projectId": config("FIREBASE_PROJECT_ID", "fastlap-155b6"),
                },
            )

        _db = firestore.client()

    return _db
