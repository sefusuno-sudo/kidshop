# 🧸 KidsShop – Magazin Online Haine Copii (0–10 ani)

Aplicație web completă pentru vânzarea hainelor de copii, construită cu **Flask** + **SQLite** + **Bootstrap 5**.

---

## 🚀 Funcționalități

| Modul | Descriere |
|-------|-----------|
| 🏠 **Pagina principală** | Produse pe categorii, oferte speciale, design pastel |
| 🛍️ **Catalog produse** | Filtrare după categorie, mărime, culoare, preț + căutare |
| 📦 **Pagina produs** | Galerie imagini, mărimi, culori, cantitate, adaugă în coș |
| 🛒 **Coș cumpărături** | Editare cantitate, ștergere, calcul total în timp real |
| 💳 **Checkout** | Formular date livrare, confirmare, notificare WhatsApp |
| 👤 **Utilizatori** | Înregistrare, login, logout, istoric comenzi |
| 🔧 **Admin Panel** | CRUD produse, vizualizare/actualizare comenzi, mesaje |
| 🌍 **Multilingv** | Română, Engleză, Rusă (Flask-Babel) |
| 📱 **WhatsApp** | Notificare automată la plasarea comenzii (Twilio) |

---

## 📁 Structura proiectului

```
kidshop/
├── app.py              # Aplicația principală Flask + factory + seed
├── config.py           # Configurații centralizate
├── extensions.py       # Inițializare extensii (db, bcrypt, babel, login)
├── models.py           # Modele SQLAlchemy (User, Product, Order, Contact)
├── forms.py            # Formulare WTForms
├── routes/
│   ├── main.py         # Pagina principală, contact, set-lang
│   ├── auth.py         # Register, login, logout, profil
│   ├── shop.py         # Catalog produse, detaliu produs
│   ├── cart.py         # Coș, actualizare, checkout, confirmare
│   └── admin.py        # Panel admin complet
├── templates/
│   ├── base.html       # Layout de bază cu navbar + footer
│   ├── index.html      # Pagina principală
│   ├── contact.html    # Formular contact
│   ├── shop/           # Catalog + detaliu produs + card produs
│   ├── cart/           # Coș + checkout + succes
│   ├── auth/           # Login + register + profil
│   └── admin/          # Dashboard + produse + comenzi + mesaje
├── static/
│   ├── css/style.css   # Design system pastel complet
│   ├── js/main.js      # JavaScript utilitar
│   └── images/         # Imagini produse
├── translations/       # Fișiere Flask-Babel (ro, en, ru)
├── .env.example        # Template variabile de mediu
├── requirements.txt    # Dependențe Python
└── database.db         # Baza de date SQLite (generată automat)
```

---

## ⚙️ Instalare & Pornire

### 1. Clonează și intră în folder
```bash
git clone <repo> kidshop
cd kidshop
```

### 2. Creează mediu virtual
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
```

### 3. Instalează dependențele
```bash
pip install -r requirements.txt
```

### 4. Configurează variabilele de mediu
```bash
cp .env.example .env
# Editează .env cu credențialele tale Twilio
```

### 5. Pornește aplicația
```bash
python app.py
```

Deschide [http://localhost:5000](http://localhost:5000) în browser.

---

## 🔐 Credențiale demo

| Rol | Email | Parolă |
|-----|-------|--------|
| **Admin** | admin@kidshop.ro | admin123 |

---

## 📱 Configurare Twilio WhatsApp

1. Creează cont pe [twilio.com](https://twilio.com)
2. Activează **WhatsApp Sandbox**
3. Completează în `.env`:
   ```
   TWILIO_ACCOUNT_SID=ACxxx...
   TWILIO_AUTH_TOKEN=xxx...
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ADMIN_WHATSAPP_TO=whatsapp:+40XXXXXXXXX
   ```

---

## 🌍 Multilingv (Flask-Babel)

Traducerile sunt configurate pentru **RO** (implicit), **EN**, **RU**.

Pentru a genera fișierele `.po`:
```bash
flask babel extract -F babel.cfg -o translations/messages.pot .
flask babel init -i translations/messages.pot -d translations -l en
flask babel compile -d translations
```

---

## 🛡️ Securitate

- Parole hash-uite cu **bcrypt**
- Protecție CSRF pe toate formularele (Flask-WTF)
- Autentificare sesiuni cu **Flask-Login**
- Acces admin protejat cu decorator `@admin_required`

---

## 🎨 Design

- **Culori pastel**: roz (#ff6b9d), bleu (#4a90d9), galben (#f5c842)
- **Font**: Nunito (Google Fonts)
- **Framework**: Bootstrap 5 (100% responsive)
- **Animații**: hover cards, floating emoji, gradiente
