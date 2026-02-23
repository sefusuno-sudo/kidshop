"""
Panel de administrare: gestionare produse, vizualizare/actualizare comenzi,
mesaje contact.
"""
import os
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, abort, current_app)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models import Product, Order, Contact, User
from forms  import ProductForm, OrderStatusForm

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator: accesibil doar pentru administratori."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return login_required(decorated)


# ─── Dashboard ────────────────────────────────────────────────────────────────
@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'total_products': Product.query.count(),
        'total_orders':   Order.query.count(),
        'pending_orders': Order.query.filter_by(status='pending').count(),
        'total_users':    User.query.count(),
        'unread_msgs':    Contact.query.filter_by(is_read=False).count(),
    }
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)


# ─── Produse ──────────────────────────────────────────────────────────────────
@admin_bp.route('/produse')
@admin_required
def products():
    all_products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=all_products)


@admin_bp.route('/produse/adauga', methods=['GET', 'POST'])
@admin_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_name = 'default.png'
        if form.image.data:
            f = form.image.data
            image_name = secure_filename(f.filename)
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))

        product = Product(
            name        = form.name.data,
            description = form.description.data,
            price       = form.price.data,
            old_price   = form.old_price.data,
            category    = form.category.data,
            sizes       = form.sizes.data,
            colors      = form.colors.data,
            age_group   = form.age_group.data,
            stock       = form.stock.data,
            is_featured = form.is_featured.data,
            is_active   = form.is_active.data,
            image       = image_name,
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Produsul "{product.name}" a fost adăugat! ✅', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, title='Adaugă produs')


@admin_bp.route('/produse/editeaza/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        if form.image.data:
            f = form.image.data
            image_name = secure_filename(f.filename)
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))
            product.image = image_name

        product.name        = form.name.data
        product.description = form.description.data
        product.price       = form.price.data
        product.old_price   = form.old_price.data
        product.category    = form.category.data
        product.sizes       = form.sizes.data
        product.colors      = form.colors.data
        product.age_group   = form.age_group.data
        product.stock       = form.stock.data
        product.is_featured = form.is_featured.data
        product.is_active   = form.is_active.data

        db.session.commit()
        flash(f'Produsul "{product.name}" a fost actualizat! ✅', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, product=product, title='Editează produs')


@admin_bp.route('/produse/sterge/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Produsul "{product.name}" a fost șters.', 'warning')
    return redirect(url_for('admin.products'))


# ─── Comenzi ──────────────────────────────────────────────────────────────────
@admin_bp.route('/comenzi')
@admin_required
def orders():
    status_filter = request.args.get('status', '')
    q = Order.query
    if status_filter:
        q = q.filter_by(status=status_filter)
    all_orders = q.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=all_orders, status_filter=status_filter)


@admin_bp.route('/comenzi/<int:order_id>', methods=['GET', 'POST'])
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    form  = OrderStatusForm(obj=order)
    if form.validate_on_submit():
        order.status = form.status.data
        db.session.commit()
        flash(f'Statusul comenzii #{order.id} a fost actualizat.', 'success')
        return redirect(url_for('admin.order_detail', order_id=order.id))
    return render_template('admin/order_detail.html', order=order, form=form)


# ─── Mesaje contact ───────────────────────────────────────────────────────────
@admin_bp.route('/mesaje')
@admin_required
def messages():
    msgs = Contact.query.order_by(Contact.created_at.desc()).all()
    # Marchează toate ca citite
    Contact.query.filter_by(is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('admin/messages.html', messages=msgs)
