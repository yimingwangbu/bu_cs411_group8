import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    GOOGLE_OAUTH_CLIENT_ID = "103466637250-l1plpeej7s1rbcgndf93f1i8k3e2ajit.apps.googleusercontent.com"
    GOOGLE_OAUTH_CLIENT_SECRET = "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"
    TMDB_API_KEY = "94011bd7028134a96aa23fdec4e62eb8"
    GOOGLE_BOOK_API_KEY = "AIzaSyB3vLdkyh2pUNn_UYdln6RLmJhUcjav49I"
