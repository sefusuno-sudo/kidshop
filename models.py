"""
Modelele bazei de date pentru KidsShop.
Definește structura tabelelor: User, Product, Order, OrderItem, Contact.
"""
from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager


# ─── User loader pentru Flask-Login ───────────────────────────────────────────
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─────────────────────────────────────────────────────────────────────────────
# MODEL: User
# ─────────────────────────────────────────────────────────────────────────────
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.String(20), default='user')  # 'user' | 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='user', lazy=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


# ─────────────────────────────────────────────────────────────────────────────
# MODEL: Product
# ─────────────────────────────────────────────────────────────────────────────
class Product(db.Model):
    __tablename__ = 'products'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price       = db.Column(db.Float, nullable=False)
    old_price   = db.Column(db.Float, nullable=True)   # pentru oferte speciale
    category    = db.Column(db.String(50), nullable=False)  # imbracaminte | incaltaminte | accesorii
    sizes       = db.Column(db.String(200), nullable=True)  # ex: "68,74,80,86,92"
    colors      = db.Column(db.String(200), nullable=True)  # ex: "rosu,albastru,verde"
    age_group   = db.Column(db.String(50), nullable=True)   # ex: "0-2 ani"
    stock       = db.Column(db.Integer, default=0)
    image       = db.Column(db.String(255), default='default.png')
    images_extra = db.Column(db.Text, nullable=True)        # JSON: imagini suplimentare
    is_featured = db.Column(db.Boolean, default=False)      # ofertă specială
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0

    @property
    def sizes_list(self):
        return [s.strip() for s in self.sizes.split(',')] if self.sizes else []

    @property
    def colors_list(self):
        return [c.strip() for c in self.colors.split(',')] if self.colors else []

    def __repr__(self):
        return f'<Product {self.name}>'


# ─────────────────────────────────────────────────────────────────────────────
# MODEL: Order
# ─────────────────────────────────────────────────────────────────────────────
class Order(db.Model):
    __tablename__ = 'orders'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    full_name    = db.Column(db.String(150), nullable=False)
    email        = db.Column(db.String(120), nullable=False)
    phone        = db.Column(db.String(20), nullable=False)
    address      = db.Column(db.Text, nullable=False)
    total        = db.Column(db.Float, nullable=False)
    status       = db.Column(db.String(30), default='pending')
    # Status posibil: pending | confirmed | shipped | delivered | cancelled
    notes        = db.Column(db.Text, nullable=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    STATUS_LABELS = {
        'pending':   ('⏳ În așteptare', 'warning'),
        'confirmed': ('✅ Confirmată',   'success'),
        'shipped':   ('🚚 Expediată',    'info'),
        'delivered': ('📦 Livrată',      'primary'),
        'cancelled': ('❌ Anulată',      'danger'),
    }

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, ('?', 'secondary'))

    def __repr__(self):
        return f'<Order #{self.id} - {self.full_name}>'


# ─────────────────────────────────────────────────────────────────────────────
# MODEL: OrderItem
# ─────────────────────────────────────────────────────────────────────────────
class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False, default=1)
    size       = db.Column(db.String(20), nullable=True)
    color      = db.Column(db.String(50), nullable=True)
    unit_price = db.Column(db.Float, nullable=False)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __repr__(self):
        return f'<OrderItem {self.product_id} x{self.quantity}>'


# ─────────────────────────────────────────────────────────────────────────────
# MODEL: Contact
# ─────────────────────────────────────────────────────────────────────────────
class Contact(db.Model):
    __tablename__ = 'contacts'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read    = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Contact {self.name}>'
