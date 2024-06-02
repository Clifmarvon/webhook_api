import firebase_admin
from firebase_admin import credentials

def initFirebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate('functions/secret.json')
        firebase_admin.initialize_app(cred)
