import os
import base64
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myFaraday', '.env')
load_dotenv(dotenv_path)

private_key = os.environ.get('firebase_private_key').replace('\\n', '\n')
private_key_bytes = private_key.encode('utf-8')
private_key_b64 = base64.b64encode(private_key_bytes)
private_key_pkcs8 = base64.b64decode(private_key_b64)

cred = credentials.Certificate({
  "type": os.environ.get('firebase_type'),
  "project_id": os.environ.get('firebase_project_id'),
  "private_key_id": os.environ.get('firebase_private_key_id'),
  "private_key": private_key_pkcs8,
  "client_email": os.environ.get('firebase_client_email'),
  "client_id": os.environ.get('firebase_client_id'),
  "auth_uri": os.environ.get('firebase_auth_uri'),
  "token_uri": os.environ.get('firebase_token_uri'),
  "auth_provider_x509_cert_url": os.environ.get('firebase_auth_provider_x509_cert_url'),
  "client_x509_cert_url": os.environ.get('firebase_client_x509_cert_url')
})

default_app = firebase_admin.initialize_app(cred, {'databaseURL': os.environ.get('FIREBASE_DATABASE_URL')})

ref = db.reference('/')
