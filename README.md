# RentEase AI — prototype

A runnable Django prototype for browsing electronic rentals, creating bookings,
tracking status, and using a rule-based rental assistant. SQLite is used by default
so it runs locally without external credentials. PostgreSQL, maps, LLM and payments
are integration points, not live integrations in this prototype.

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ . Admin: /admin/

## Prototype flows
- Browse seeded products on the home page.
- Register/login with Django authentication.
- Book a product with dates; overlapping active reservations are rejected.
- View your bookings and advance the status in the demo UI.
- Ask the assistant for products by keyword/budget (rule-based, no LLM credentials).

This is a demo foundation, not production-ready. Before deployment add PostgreSQL,
proper role/ownership permissions, payment-provider signature verification, real
geospatial search, a configured LLM, notifications, comprehensive tests, and
production settings/HTTPS.
