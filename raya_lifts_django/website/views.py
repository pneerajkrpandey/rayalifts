from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .forms import EnquiryForm
from .models import Category, Product, Page, LiftProject, SiteSettings, Service, Testimonial, HomeSection, CustomSection

def home(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True, category__is_active=True)[:6]
    projects = LiftProject.objects.filter(is_active=True, show_on_website=True, client__is_active=True)[:6]
    pages = Page.objects.filter(is_active=True, show_in_navigation=True)[:4]
    services = Service.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    hero_slides = []  # The site settings hero image can be replaced from the admin without editing templates.
    return render(request, "website/home.html", {
        "categories": categories,
        "featured_products": featured_products,
        "projects": projects,
        "pages": pages,
        "services": services,
        "testimonials": testimonials,
        "hero_slides": hero_slides,
    })

def about(request):
    page = Page.objects.filter(is_active=True, slug="about").first()
    return render(request, "website/about.html", {"page": page})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_active=True)
    return render(request, "website/page_detail.html", {"page": page})

def catalog(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related("category")
    selected_category = request.GET.get("category", "")
    search_query = request.GET.get("q", "").strip()
    if selected_category:
        products = products.filter(category__slug=selected_category)
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(summary__icontains=search_query) | Q(description__icontains=search_query))
    return render(request, "website/catalog.html", {
        "categories": categories,
        "products": products,
        "selected_category": selected_category,
        "search_query": search_query,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)
    return render(request, "website/category_detail.html", {"category": category, "products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True, category__is_active=True)
    return render(request, "website/product_detail.html", {"product": product, "specification_lines": [line.strip() for line in product.specifications.splitlines() if line.strip()]})

def projects(request):
    project_list = LiftProject.objects.filter(is_active=True, show_on_website=True, client__is_active=True)
    return render(request, "website/projects.html", {"projects": project_list})

def contact(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            site = SiteSettings.objects.first()
            recipient = (site.contact_email if site and site.contact_email else settings.CONTACT_EMAIL)
            subject = f"New Raya Lifts enquiry from {enquiry.name}"
            body = (
                f"New website enquiry\\n\\nName: {enquiry.name}\\nPhone: {enquiry.phone}\\n"
                f"Email: {enquiry.email or 'Not provided'}\\nCity: {enquiry.city or 'Not provided'}\\n"
                f"Lift interest: {enquiry.lift_interest or 'Not specified'}\\n\\nMessage:\\n{enquiry.message}"
            )
            try:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False)
                messages.success(request, "Thank you. Your enquiry has been sent successfully.")
            except Exception:
                # Enquiry is still safely stored in admin even if email configuration needs attention.
                messages.warning(request, "Thank you. Your enquiry was saved. Our team will follow up shortly.")
            return redirect("contact")
    else:
        form = EnquiryForm()
    return render(request, "website/contact.html", {"form": form})

def robots_txt(request):
    from django.http import HttpResponse
    return HttpResponse(f"User-agent: *\\nAllow: /\\nSitemap: {settings.SITE_URL}/sitemap.xml\\n", content_type="text/plain")

def sitemap_xml(request):
    from django.http import HttpResponse
    from django.utils.html import escape
    urls = [settings.SITE_URL, f"{settings.SITE_URL}/about/", f"{settings.SITE_URL}/catalog/", f"{settings.SITE_URL}/projects/", f"{settings.SITE_URL}/contact/"]
    urls += [f"{settings.SITE_URL}{p.get_absolute_url()}" for p in Product.objects.filter(is_active=True, category__is_active=True)]
    urls += [f"{settings.SITE_URL}{c.get_absolute_url()}" for c in Category.objects.filter(is_active=True)]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f"<url><loc>{escape(url)}</loc></url>" for url in urls) + "</urlset>"
    return HttpResponse(xml, content_type="application/xml")
