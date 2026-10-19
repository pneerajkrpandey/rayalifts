# Raya Lifts — Premium Django Website (Fresh UI)

This is a fresh redesign based on the user-provided Raya Lifts website mockup: dark navy header, gold accents, full-bleed architectural hero slideshow, trust strip, lift category cards, project gallery, product collection, service cards, testimonials, CTA and responsive footer. It is not the previous ZIP's UI.

## Requirements
- Python 3.10+
- Internet connection for Google Fonts (all default lift demo images are bundled locally)

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations website
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/.

## Admin content
Use Django Admin to edit site settings/logo/hero copy and all three hero slides, categories, products, project/client records, service images, testimonials and enquiries. Under Site Settings → Design theme, change the site-wide navy, gold, surface and text colours and choose a font. Under Custom homepage sections, each added section has its own background, text and accent colours plus font choice. The Header and Footer controls let you switch the global header/footer and WhatsApp float on/off. Homepage section visibility lets you switch built-in sections on/off; Custom homepage sections lets you add extra image/text/CTA sections, set their order, and publish/unpublish them without editing code. Upload your licensed/owned product and project photos through the relevant image fields. Sample projects and testimonials are dummy content and must be replaced with genuine information before launch.

## Images
Bundled local lift-image placeholders are cropped from the supplied Raya Lifts reference screenshot, so the site does not depend on remote stock-photo URLs to show the initial lift imagery. Upload full-resolution photos you own or have permission to use in Site Settings, Categories, Products, Projects, Services and Custom Sections to replace these small reference crops before launch. The provided screenshot does not include the original full-resolution source photographs.

## Email
The default Django email backend prints messages to the terminal. Configure SMTP in the environment for real delivery. `CONTACT_EMAIL` can be set as the recipient; check `config/settings.py` for available environment variables. Enquiries are stored in Django Admin even if email delivery is not configured.

## Production checklist
- Set a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS`.
- Configure a production database, SMTP, HTTPS, static/media hosting and backups.
- Replace all demo data, sample testimonials, contact details and stock/demo imagery.
- Review lift technical specifications and any safety/certification claims before publishing.

The demo counters are visual placeholders, not verified company statistics.
