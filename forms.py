"""
Formularele aplicației folosind Flask-WTF și WTForms.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, TextAreaField, FloatField,
                     IntegerField, SelectField, BooleanField, TelField, SubmitField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange, ValidationError
from models import User


# ─── Autentificare ────────────────────────────────────────────────────────────
class RegisterForm(FlaskForm):
    username  = StringField('Nume utilizator', validators=[DataRequired(), Length(3, 80)])
    email     = StringField('Email', validators=[DataRequired(), Email()])
    password  = PasswordField('Parolă', validators=[DataRequired(), Length(6)])
    password2 = PasswordField('Confirmă parola', validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField('Înregistrare')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Numele de utilizator este deja folosit.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Adresa de email este deja înregistrată.')


class LoginForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Parolă', validators=[DataRequired()])
    remember = BooleanField('Ține-mă minte')
    submit   = SubmitField('Autentificare')


# ─── Checkout ─────────────────────────────────────────────────────────────────
class CheckoutForm(FlaskForm):
    full_name = StringField('Nume complet', validators=[DataRequired(), Length(3, 150)])
    email     = StringField('Email', validators=[DataRequired(), Email()])
    phone     = TelField('Telefon', validators=[DataRequired(), Length(7, 20)])
    address   = TextAreaField('Adresă livrare', validators=[DataRequired(), Length(10, 300)])
    notes     = TextAreaField('Observații', validators=[Optional(), Length(max=500)])
    submit    = SubmitField('Plasează comanda')


# ─── Contact ──────────────────────────────────────────────────────────────────
class ContactForm(FlaskForm):
    name    = StringField('Nume', validators=[DataRequired(), Length(2, 100)])
    email   = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Mesaj', validators=[DataRequired(), Length(10, 1000)])
    submit  = SubmitField('Trimite mesajul')


# ─── Admin – Produs ───────────────────────────────────────────────────────────
CATEGORIES = [
    ('imbracaminte', 'Îmbrăcăminte'),
    ('incaltaminte', 'Încălțăminte'),
    ('accesorii',   'Accesorii'),
]

class ProductForm(FlaskForm):
    name        = StringField('Denumire produs', validators=[DataRequired(), Length(2, 150)])
    description = TextAreaField('Descriere', validators=[Optional()])
    price       = FloatField('Preț (RON)', validators=[DataRequired(), NumberRange(min=0)])
    old_price   = FloatField('Preț vechi (RON)', validators=[Optional(), NumberRange(min=0)])
    category    = SelectField('Categorie', choices=CATEGORIES, validators=[DataRequired()])
    sizes       = StringField('Mărimi (ex: 68,74,80)', validators=[Optional()])
    colors      = StringField('Culori (ex: rosu,albastru)', validators=[Optional()])
    age_group   = StringField('Grup de vârstă (ex: 0-2 ani)', validators=[Optional()])
    stock       = IntegerField('Stoc', validators=[NumberRange(min=0)], default=0)
    is_featured = BooleanField('Ofertă specială')
    is_active   = BooleanField('Produs activ', default=True)
    image       = FileField('Imagine principală', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Doar imagini!')])
    submit      = SubmitField('Salvează produsul')


# ─── Admin – Status comandă ───────────────────────────────────────────────────
class OrderStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending',   '⏳ În așteptare'),
        ('confirmed', '✅ Confirmată'),
        ('shipped',   '🚚 Expediată'),
        ('delivered', '📦 Livrată'),
        ('cancelled', '❌ Anulată'),
    ])
    submit = SubmitField('Actualizează')
