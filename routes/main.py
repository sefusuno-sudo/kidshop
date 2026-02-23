"""
Rutele principale: pagina de start, contact, schimbare limbă.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Product, Contact
from forms  import ContactForm
from extensions import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Pagina principală cu produse pe categorii și oferte speciale."""
    featured    = Product.query.filter_by(is_featured=True, is_active=True).limit(6).all()
    imbracaminte = Product.query.filter_by(category='imbracaminte', is_active=True).limit(4).all()
    incaltaminte = Product.query.filter_by(category='incaltaminte', is_active=True).limit(4).all()
    accesorii    = Product.query.filter_by(category='accesorii',    is_active=True).limit(4).all()
    return render_template('index.html',
                           featured=featured,
                           imbracaminte=imbracaminte,
                           incaltaminte=incaltaminte,
                           accesorii=accesorii)


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Pagina de contact cu formular salvat în baza de date."""
    form = ContactForm()
    if form.validate_on_submit():
        msg = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Mesajul tău a fost trimis! Te vom contacta în curând. 💌', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)


@main_bp.route('/set-lang/<lang>')
def set_lang(lang):
    """Schimbă limba aplicației."""
    from config import Config
    if lang in Config.LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))
