import os
import firebase_admin
from firebase_admin import credentials, firestore
from .config import FIREBASE_CREDENTIALS_PATH

_db = None


def get_db():
    global _db
    if _db is None:
        if not firebase_admin._apps:
            if FIREBASE_CREDENTIALS_PATH:
                abs_path = os.path.abspath(FIREBASE_CREDENTIALS_PATH)
                if not os.path.exists(abs_path):
                    raise FileNotFoundError(
                        f"Firebase credentials file not found at '{abs_path}'. "
                        "Please download serviceAccountKey.json from Firebase Console "
                        "(Project Settings > Service Accounts > Generate New Private Key) "
                        "and place it in your project directory."
                    )
                cred = credentials.Certificate(abs_path)
                firebase_admin.initialize_app(cred)
                print(f"Firebase connected successfully using: {abs_path}")
            else:
                raise ValueError("FIREBASE_CREDENTIALS_PATH not configured in .env")
        _db = firestore.client()
    return _db


def is_initialized():
    try:
        get_db()
        return True
    except Exception:
        return False


def get_existing_ids(collection_name):
    try:
        db = get_db()
        docs = db.collection(collection_name).stream()
        return {doc.id for doc in docs}
    except Exception as e:
        print(f"Error fetching from Firebase: {e}")
        return set()


def add_entry(collection_name, data, doc_id=None):
    try:
        db = get_db()
        if doc_id:
            doc_ref = db.collection(collection_name).document(doc_id)
        else:
            doc_ref = db.collection(collection_name).document()
        doc_ref.set(data)
        print(f"Success! '{data.get('title', 'Untitled')}' has been added to Firebase.")
        return True
    except Exception as e:
        print(f"Error {e}")
        return False