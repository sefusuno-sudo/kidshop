"""
Configurația aplicației KidsShop.
Setările sunt citite din variabile de mediu (.env) sau valori implicite.
"""
import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ─── Securitate ───────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY', 'kidshop-super-secret-key-2024')

    # ─── Baza de date ─────────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'database.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ─── Upload fișiere ───────────────────────────────────────────────────────
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'images', 'products')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # ─── Multilingv (Flask-Babel) ─────────────────────────────────────────────
    LANGUAGES = ['ro', 'en', 'ru']
    BABEL_DEFAULT_LOCALE = 'ro'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Bucharest'

    # ─── Twilio WhatsApp ──────────────────────────────────────────────────────
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN  = os.environ.get('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
    ADMIN_WHATSAPP_TO    = os.environ.get('ADMIN_WHATSAPP_TO', 'whatsapp:+40700000000')

    # ─── Paginare ─────────────────────────────────────────────────────────────
    PRODUCTS_PER_PAGE = 12
