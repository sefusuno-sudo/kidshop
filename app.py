"""
KidsShop – Magazin online haine copii (0–10 ani)
Backend: Flask | DB: SQLite + SQLAlchemy | Auth: Flask-Login + bcrypt
Multilingv: Flask-Babel (RO, EN, RU) | WhatsApp: Twilio
"""
import os, json
from datetime import datetime
from flask import (Flask, render_template, redirect, url_for, request,
                   flash, session, jsonify, abort, g)
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import gettext as _, get_locale
from werkzeug.utils import secure_filename

from config    import Config
from extensions import db, login_manager, bcrypt, babel
from models    import User, Product, Order, OrderItem, Contact
from forms     import (RegisterForm, LoginForm, CheckoutForm,
                       ContactForm, ProductForm, OrderStatusForm)


# ─────────────────────────────────────────────────────────────────────────────
# Factory & inițializare
# ─────────────────────────────────────────────────────────────────────────────
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inițializare extensii
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    babel.init_app(app, locale_selector=get_locale_selector)

    # Creare folder upload dacă nu există
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # ── Variabile globale pentru template-uri ──────────────────────────────
    @app.context_processor
    def inject_globals():
        cart = session.get('cart', {})
        cart_count = sum(item['quantity'] for item in cart.values())
        return dict(
            cart_count=cart_count,
            current_locale=str(get_locale()),
            now=datetime.utcnow(),
        )

    # ── Creare tabele și date inițiale ────────────────────────────────────
    with app.app_context():
        db.create_all()
        seed_demo_data()

    # Înregistrare blueprint-uri
    register_blueprints(app)
    return app


def get_locale_selector():
    """Selectează limba din sesiune sau Accept-Language header."""
    lang = session.get('lang')
    if lang in Config.LANGUAGES:
        return lang
    return request.accept_languages.best_match(Config.LANGUAGES) or 'ro'


def register_blueprints(app):
    """Înregistrează toate rutele în blueprint-uri."""
    from routes.main  import main_bp
    from routes.auth  import auth_bp
    from routes.shop  import shop_bp
    from routes.cart  import cart_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,  url_prefix='/auth')
    app.register_blueprint(shop_bp,  url_prefix='/shop')
    app.register_blueprint(cart_bp,  url_prefix='/cart')
    app.register_blueprint(admin_bp, url_prefix='/admin')


# ─────────────────────────────────────────────────────────────────────────────
# Date demo (seed)
# ─────────────────────────────────────────────────────────────────────────────
def seed_demo_data():
    """Populează baza de date cu date demo dacă e goală."""
    if User.query.first():
        return  # deja seeded

    # Admin implicit
    admin_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
    admin = User(username='admin', email='admin@kidshop.ro',
                 password=admin_pw, role='admin')
    db.session.add(admin)

    # Produse demo
    products = [
        dict(name='Body Bumbac Organic', description='Body moale din bumbac 100% organic, perfect pentru bebeluși.',
             price=49.99, old_price=69.99, category='imbracaminte',
             sizes='56,62,68,74', colors='alb,roz,bleu', age_group='0-1 an',
             stock=25, image='body1.png', is_featured=True),
        dict(name='Set Compleu Primăvară', description='Set trendy pentru copii activi, rezistent la uzură.',
             price=89.99, category='imbracaminte',
             sizes='80,86,92,98,104', colors='galben,verde,portocaliu', age_group='1-3 ani',
             stock=15, image='set1.png', is_featured=False),
        dict(name='Rochie Floricele', description='Rochie elegantă cu imprimeu floral, ideală pentru ocazii.',
             price=119.99, old_price=149.99, category='imbracaminte',
             sizes='92,98,104,110,116', colors='roz,lila', age_group='3-5 ani',
             stock=10, image='rochie1.png', is_featured=True),
        dict(name='Pantofi Sport Colorați', description='Pantofi ușori și flexibili, perfecti pentru primii pași.',
             price=79.99, category='incaltaminte',
             sizes='18,19,20,21,22', colors='rosu,albastru,verde', age_group='1-2 ani',
             stock=20, image='pantofi1.png', is_featured=False),
        dict(name='Cizmuliţe Ploaie', description='Cizme impermeabile cu personaje vesele.',
             price=99.99, old_price=129.99, category='incaltaminte',
             sizes='24,25,26,27,28', colors='galben,roz', age_group='3-6 ani',
             stock=12, image='cizme1.png', is_featured=True),
        dict(name='Adidași Velcro', description='Adidași comozi cu închidere velcro, ușor de pus.',
             price=139.99, category='incaltaminte',
             sizes='29,30,31,32,33', colors='alb,negru,albastru', age_group='5-8 ani',
             stock=18, image='adidasi1.png', is_featured=False),
        dict(name='Pălărie Soare UV50+', description='Pălărie protecție UV pentru zilele însorite.',
             price=34.99, category='accesorii',
             sizes='XS,S,M', colors='albastru,roz,alb,galben', age_group='0-5 ani',
             stock=30, image='palarie1.png', is_featured=False),
        dict(name='Rucsac Dinozaur', description='Rucsac mic și adorabil în formă de dinozaur.',
             price=59.99, old_price=79.99, category='accesorii',
             sizes='One Size', colors='verde,mov', age_group='2-6 ani',
             stock=22, image='rucsac1.png', is_featured=True),
        dict(name='Șapcă Baseball', description='Șapcă reglabilă cu protecție solară.',
             price=24.99, category='accesorii',
             sizes='48-52cm,52-56cm', colors='rosu,albastru,negru', age_group='3-10 ani',
             stock=35, image='sapca1.png', is_featured=False),
    ]

    for p in products:
        db.session.add(Product(**p))

    db.session.commit()
    print("✅ Date demo adăugate cu succes!")


# ─────────────────────────────────────────────────────────────────────────────
# Utilitare globale
# ─────────────────────────────────────────────────────────────────────────────
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def send_whatsapp_notification(order: Order):
    """Trimite notificare WhatsApp prin Twilio la plasarea comenzii."""
    try:
        from twilio.rest import Client
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        items_text = '\n'.join(
            f"  • {item.product.name} x{item.quantity} = {item.subtotal:.2f} RON"
            for item in order.items
        )
        body = (
            f"🛍️ *Comandă nouă #{order.id}* – KidsShop\n\n"
            f"👤 {order.full_name}\n"
            f"📱 {order.phone}\n"
            f"📧 {order.email}\n"
            f"📍 {order.address}\n\n"
            f"🛒 Produse:\n{items_text}\n\n"
            f"💰 *Total: {order.total:.2f} RON*"
        )
        client.messages.create(
            body=body,
            from_=Config.TWILIO_WHATSAPP_FROM,
            to=Config.ADMIN_WHATSAPP_TO
        )
        print(f"📲 WhatsApp trimis pentru comanda #{order.id}")
    except Exception as e:
        print(f"⚠️ Eroare WhatsApp: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Pornire aplicație
# ─────────────────────────────────────────────────────────────────────────────
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
