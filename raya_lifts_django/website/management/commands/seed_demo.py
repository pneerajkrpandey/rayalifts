from django.core.management.base import BaseCommand
from website.models import SiteSettings, Category, Product, Service, Testimonial, Client, LiftProject, HomeSection

class Command(BaseCommand):
    help = "Create editable dummy content for the Raya Lifts redesign."
    def handle(self, *args, **options):
        site, _ = SiteSettings.objects.get_or_create(company_name="Raya Lifts", defaults={
            "tagline": "Elevating Your World", "phone": "+91 98765 43210", "email": "info@rayalifts.in",
            "whatsapp_number": "919876543210", "address": "Lucknow, Uttar Pradesh, India",
            "hero_title": "Safe. Smart. Stylish. Raya Lifts.",
            "hero_subtitle": "We design and deliver world-class elevator solutions for residential, commercial, and industrial spaces. Experience the perfect blend of technology, safety, and elegance.",
            "footer_text": "Premium lift solutions for homes, businesses and modern spaces.",
            "about_heading": "Built around your journey",
            "about_text": "Raya Lifts delivers carefully planned vertical mobility solutions with a focus on safety, thoughtful design and dependable support.",
            "experience_label": "Thoughtful design. Dependable service.",
        })
        category_rows = [
            ("Home Lifts", "home-lifts", "Comfort and convenience for your dream home."),
            ("Passenger Lifts", "passenger-lifts", "Smooth and efficient movement for modern buildings."),
            ("Commercial Lifts", "commercial-lifts", "Built for performance and high traffic."),
            ("Goods Lifts", "goods-lifts", "Heavy-duty solutions for business and warehouse spaces."),
            ("Hospital Lifts", "hospital-lifts", "Thoughtful movement for care environments."),
        ]
        for order, key in enumerate(["trust", "categories", "projects", "products", "services", "testimonials", "cta"]):
            HomeSection.objects.get_or_create(key=key, defaults={"is_active": True, "display_order": order})

        cats = {}
        for name, slug, desc in category_rows:
            cats[slug], _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "short_description": desc, "description": desc, "is_active": True})
        product_rows = [
            ("Raya Home Lift", "raya-home-lift", "A refined home lift concept for modern residences.", "home-lifts", True),
            ("Raya Panoramic Lift", "raya-panoramic-lift", "A glass-cabin concept that brings light and openness to interiors.", "home-lifts", True),
            ("Raya Passenger Lift", "raya-passenger-lift", "Dependable passenger mobility for apartments and offices.", "passenger-lifts", True),
            ("Raya Commercial Lift", "raya-commercial-lift", "A practical solution for retail, office and hospitality spaces.", "commercial-lifts", True),
            ("Raya Goods Lift", "raya-goods-lift", "A robust lift concept for goods movement and warehouse use.", "goods-lifts", True),
            ("Raya Care Lift", "raya-care-lift", "Designed around reliable movement in care settings.", "hospital-lifts", False),
        ]
        for i, (name, slug, desc, cat, featured) in enumerate(product_rows):
            Product.objects.get_or_create(slug=slug, defaults={"name": name, "summary": desc, "description": desc + " Sample copy for the demo website. Confirm all specifications with your technical team before publishing.", "category": cats[cat], "is_active": True, "is_featured": featured, "display_order": i})
        service_rows = [
            ("Lift installation", "Professional planning, installation and commissioning.", "↗"),
            ("Maintenance & repairs", "Ongoing support to help keep your lift operating smoothly.", "⚙"),
            ("Modernisation", "Refresh existing lifts with updated controls and finishes.", "✦"),
            ("Home lift solutions", "Space-conscious options for villas and private residences.", "⌂"),
            ("Custom cabin design", "Cabin finishes selected to complement your building.", "◇"),
            ("Lift consultation", "Guidance to help identify the right solution for your project.", "＋"),
        ]
        for i, (title, summary, icon) in enumerate(service_rows):
            Service.objects.get_or_create(slug=title.lower().replace(" ", "-"), defaults={"title": title, "summary": summary, "icon": icon, "display_order": i, "is_active": True})
        reviews = [
            ("Aarav Sharma", "Homeowner · Lucknow", "The team explained the available options clearly and guided us through the process."),
            ("Priya Mehta", "Property manager · Noida", "Communication was straightforward, and the installation planning felt organised."),
            ("Karan Verma", "Business owner · Delhi NCR", "A professional experience from the first conversation through to handover."),
        ]
        for i, (name, role, quote) in enumerate(reviews):
            Testimonial.objects.get_or_create(customer_name=name, defaults={"role_or_location": role, "quote": quote, "rating": 5, "display_order": i, "is_active": True})
        projects = [
            ("Luxury Residence", "Gurugram, Haryana", "Home Lift"),
            ("Office Building", "Noida, Uttar Pradesh", "Passenger Lift"),
            ("Shopping Mall", "Delhi NCR", "Commercial Lift"),
            ("Warehouse Facility", "Faridabad, Haryana", "Goods Lift"),
            ("Care Centre", "Lucknow, Uttar Pradesh", "Hospital Lift"),
        ]
        for i, (title, location, lift_type) in enumerate(projects):
            client, _ = Client.objects.get_or_create(company_or_property=title, defaults={"name": "Demo Client", "location": location, "is_active": True})
            LiftProject.objects.get_or_create(title=title, defaults={"client": client, "lift_type": lift_type, "location": location, "description": "DEMO PORTFOLIO ENTRY — replace with a real Raya Lifts installation before launch.", "status": "completed", "show_on_website": True, "is_active": True, "display_order": i})
        self.stdout.write(self.style.SUCCESS("Demo content created. Replace sample testimonials and project entries before launch."))
