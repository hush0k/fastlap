from pathlib import Path
from typing import Optional

import firebase_admin
from decouple import config
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client

_app: Optional[firebase_admin.App] = None
_db: Optional[Client] = None


def get_firestore_client() -> Client:
    """Get or create Firestore client singleton."""
    global _app, _db

    if _db is None:
        try:
            _app = firebase_admin.get_app()
        except ValueError:
            cred_path: Path = Path(__file__).parent / "firebase-credentials.json"
            cred: credentials.Certificate = credentials.Certificate(str(cred_path))

            _app = firebase_admin.initialize_app(
                cred,
                {
                    "projectId": config("FIREBASE_PROJECT_ID", "fastlap-155b6"),
                },
            )

        _db = firestore.client()

    return _db