from .models import SiteSettings, Page, Category, HomeSection, CustomSection, SocialLink, HeroSection

def site_settings(request):
    settings_obj = SiteSettings.objects.first()
    navigation_pages = Page.objects.filter(is_active=True, show_in_navigation=True)
    navigation_categories = Category.objects.filter(is_active=True)
    section_rows = HomeSection.objects.filter(is_active=True).values_list("key", flat=True)
    # A fresh install should display every built-in homepage section before the admin is configured.
    if HomeSection.objects.exists():
        active_section_keys = list(section_rows)
    else:
        active_section_keys = ["trust", "categories", "projects", "products", "services", "testimonials", "cta"]
    return {
        "site_settings": settings_obj,
        "navigation_pages": navigation_pages,
        "navigation_categories": navigation_categories,
        "active_section_keys": active_section_keys,
        "custom_home_sections": CustomSection.objects.filter(is_active=True).order_by("display_order", "id"),
        "social_links": SocialLink.objects.filter(is_active=True).exclude(url="").order_by("display_order", "id"),
        "hero_sections": {hero.page_key: hero for hero in HeroSection.objects.filter(is_active=True)},
    }
