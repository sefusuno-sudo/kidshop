"""
Rutele coșului de cumpărături și finalizare comandă.
Coșul este stocat în sesiunea Flask (session).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import (Blueprint, render_template, redirect, url_for,
                   flash, session, request, jsonify)
from flask_login import current_user
from extensions import db
from models import Product, Order, OrderItem
from forms  import CheckoutForm

cart_bp = Blueprint('cart', __name__)


def get_cart():
    """Returnează coșul curent din sesiune."""
    return session.get('cart', {})


def save_cart(cart):
    """Salvează coșul în sesiune."""
    session['cart'] = cart
    session.modified = True


def cart_total(cart):
    """Calculează totalul coșului."""
    total = 0
    for key, item in cart.items():
        product = Product.query.get(item['product_id'])
        if product:
            total += product.price * item['quantity']
    return round(total, 2)


# ─── Vizualizare coș ──────────────────────────────────────────────────────────
@cart_bp.route('/')
def view_cart():
    cart = get_cart()
    items = []
    for key, item in cart.items():
        product = Product.query.get(item['product_id'])
        if product:
            items.append({
                'key':      key,
                'product':  product,
                'quantity': item['quantity'],
                'size':     item.get('size', ''),
                'color':    item.get('color', ''),
                'subtotal': round(product.price * item['quantity'], 2),
            })
    total = sum(i['subtotal'] for i in items)
    return render_template('cart/cart.html', items=items, total=round(total, 2))


# ─── Adaugă în coș ────────────────────────────────────────────────────────────
@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product  = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    size     = request.form.get('size', '')
    color    = request.form.get('color', '')

    cart = get_cart()
    key  = f"{product_id}_{size}_{color}"  # cheie unică per produs+mărime+culoare

    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'product_id': product_id,
            'quantity':   quantity,
            'size':       size,
            'color':      color,
        }

    save_cart(cart)
    flash(f'"{product.name}" a fost adăugat în coș! 🛒', 'success')
    return redirect(request.referrer or url_for('cart.view_cart'))


# ─── Actualizează cantitate ───────────────────────────────────────────────────
@cart_bp.route('/update/<key>', methods=['POST'])
def update_cart(key):
    cart     = get_cart()
    quantity = int(request.form.get('quantity', 1))

    if key in cart:
        if quantity <= 0:
            del cart[key]
            flash('Produs eliminat din coș.', 'info')
        else:
            cart[key]['quantity'] = quantity

    save_cart(cart)
    return redirect(url_for('cart.view_cart'))


# ─── Elimină din coș ──────────────────────────────────────────────────────────
@cart_bp.route('/remove/<key>', methods=['POST'])
def remove_from_cart(key):
    cart = get_cart()
    if key in cart:
        del cart[key]
        save_cart(cart)
        flash('Produs eliminat din coș.', 'info')
    return redirect(url_for('cart.view_cart'))


# ─── Checkout ─────────────────────────────────────────────────────────────────
@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = get_cart()
    if not cart:
        flash('Coșul tău este gol!', 'warning')
        return redirect(url_for('shop.products'))

    form = CheckoutForm()

    # Pre-completare date dacă utilizatorul e logat
    if request.method == 'GET' and current_user.is_authenticated:
        form.email.data = current_user.email

    if form.validate_on_submit():
        # Calculare total
        total = 0
        order_items = []
        for key, item in cart.items():
            product = Product.query.get(item['product_id'])
            if product:
                subtotal = product.price * item['quantity']
                total += subtotal
                order_items.append(OrderItem(
                    product_id = product.id,
                    quantity   = item['quantity'],
                    size       = item.get('size', ''),
                    color      = item.get('color', ''),
                    unit_price = product.price,
                ))

        # Creare comandă
        order = Order(
            user_id   = current_user.id if current_user.is_authenticated else None,
            full_name = form.full_name.data,
            email     = form.email.data,
            phone     = form.phone.data,
            address   = form.address.data,
            notes     = form.notes.data,
            total     = round(total, 2),
        )
        db.session.add(order)
        db.session.flush()  # obținem order.id înainte de commit

        for oi in order_items:
            oi.order_id = order.id
            db.session.add(oi)

        db.session.commit()

        # Trimite notificare WhatsApp
        from app import send_whatsapp_notification
        send_whatsapp_notification(order)

        # Golire coș
        session.pop('cart', None)

        flash(f'Comanda #{order.id} a fost plasată cu succes! 🎉 Te vom contacta în curând.', 'success')
        return redirect(url_for('cart.order_success', order_id=order.id))

    # Construire preview items pentru pagina checkout
    items = []
    for key, item in cart.items():
        product = Product.query.get(item['product_id'])
        if product:
            items.append({
                'product':  product,
                'quantity': item['quantity'],
                'size':     item.get('size', ''),
                'subtotal': round(product.price * item['quantity'], 2),
            })
    total = sum(i['subtotal'] for i in items)

    return render_template('cart/checkout.html', form=form, items=items, total=round(total, 2))


@cart_bp.route('/success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('cart/order_success.html', order=order)
