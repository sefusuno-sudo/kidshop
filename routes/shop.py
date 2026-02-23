"""
Rutele magazinului: listare produse, filtrare, căutare, pagina produs.
"""
from flask import Blueprint, render_template, request, abort
from models import Product
from config import Config

shop_bp = Blueprint('shop', __name__)


@shop_bp.route('/')
@shop_bp.route('/categoria/<category>')
def products(category=None):
    """Listare produse cu filtre: categorie, mărime, culoare, preț, căutare."""
    query = Product.query.filter_by(is_active=True)

    # Filtru categorie
    if category and category in ('imbracaminte', 'incaltaminte', 'accesorii'):
        query = query.filter_by(category=category)

    # Căutare text
    search = request.args.get('q', '').strip()
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    # Filtru mărime
    size = request.args.get('size', '').strip()
    if size:
        query = query.filter(Product.sizes.ilike(f'%{size}%'))

    # Filtru culoare
    color = request.args.get('color', '').strip()
    if color:
        query = query.filter(Product.colors.ilike(f'%{color}%'))

    # Filtru preț
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)

    # Sortare
    sort = request.args.get('sort', 'newest')
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    # Paginare
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=Config.PRODUCTS_PER_PAGE, error_out=False)
    products = pagination.items

    return render_template('shop/products.html',
                           products=products,
                           pagination=pagination,
                           category=category,
                           search=search,
                           size=size, color=color,
                           price_min=price_min, price_max=price_max,
                           sort=sort)


@shop_bp.route('/produs/<int:product_id>')
def product_detail(product_id):
    """Pagina detaliată a unui produs."""
    product = Product.query.get_or_404(product_id)
    if not product.is_active:
        abort(404)

    # Produse similare (aceeași categorie)
    related = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()

    return render_template('shop/product_detail.html',
                           product=product,
                           related=related)
