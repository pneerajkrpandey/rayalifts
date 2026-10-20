from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SiteSettings(TimeStampedModel):
    company_name = models.CharField(max_length=150, default="Raya Lifts")
    tagline = models.CharField(max_length=220, default="Moving you forward.")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True, help_text="International format, digits only, e.g. 919876543210")
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    footer_text = models.CharField(max_length=250, blank=True, default="Reliable lift solutions for homes and businesses.")
    hero_title = models.CharField(max_length=220, default="Elevating the way you move")
    hero_subtitle = models.TextField(default="Thoughtfully designed lift solutions for homes, businesses and modern spaces.")
    hero_image = models.ImageField(upload_to="site/", blank=True, null=True)
    hero_image_2 = models.ImageField(upload_to="site/", blank=True, null=True, help_text="Optional second hero slide image.")
    hero_image_3 = models.ImageField(upload_to="site/", blank=True, null=True, help_text="Optional third hero slide image.")
    about_heading = models.CharField(max_length=220, default="Built around your journey")
    about_text = models.TextField(blank=True, default="Raya Lifts delivers practical, carefully planned vertical mobility solutions with a focus on safety, service and dependable installation.")
    experience_label = models.CharField(max_length=80, blank=True, default="Quality-focused lift solutions")
    primary_cta_text = models.CharField(max_length=80, default="Request a consultation")
    primary_cta_url = models.CharField(max_length=200, default="/contact/")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    show_header = models.BooleanField(default=True, help_text="Turn the full site header on or off.")
    show_footer = models.BooleanField(default=True, help_text="Turn the full site footer on or off.")
    show_whatsapp_button = models.BooleanField(default=True)
    contact_email = models.EmailField(blank=True, help_text="Enquiry notification recipient. Falls back to CONTACT_EMAIL in environment.")
    theme_navy = models.CharField(max_length=7, default="#101a2a", help_text="Hex colour, e.g. #101a2a")
    theme_gold = models.CharField(max_length=7, default="#d5a12b", help_text="Hex colour, e.g. #d5a12b")
    theme_surface = models.CharField(max_length=7, default="#f5f6f8", help_text="Default section background colour")
    theme_text = models.CharField(max_length=7, default="#101a2a", help_text="Main text colour")
    theme_font = models.CharField(max_length=20, choices=[("Manrope", "Manrope"), ("DM Sans", "DM Sans"), ("Montserrat", "Montserrat")], default="Manrope")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            self.pk = SiteSettings.objects.first().pk
        super().save(*args, **kwargs)

class Page(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    intro = models.TextField(blank=True)
    body = models.TextField(blank=True, help_text="Plain text content; line breaks are preserved.")
    featured_image = models.ImageField(upload_to="pages/", blank=True, null=True)
    show_in_navigation = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    hero_title = models.CharField(max_length=220, blank=True)
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="pages/hero/", blank=True, null=True)
    hero_cta_text = models.CharField(max_length=80, blank=True)
    hero_cta_url = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["display_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Category(TimeStampedModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=260, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    gallery_image_2 = models.ImageField(upload_to="products/gallery/", blank=True, null=True)
    gallery_image_3 = models.ImageField(upload_to="products/gallery/", blank=True, null=True)
    specifications = models.TextField(blank=True, help_text="One specification per line, e.g. Capacity: 6 persons")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["display_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

class Client(TimeStampedModel):
    name = models.CharField(max_length=160)
    company_or_property = models.CharField(max_length=180, blank=True)
    location = models.CharField(max_length=180, blank=True)
    private_phone = models.CharField(max_length=40, blank=True, help_text="Private: never shown publicly.")
    private_email = models.EmailField(blank=True, help_text="Private: never shown publicly.")
    internal_notes = models.TextField(blank=True, help_text="Private admin-only notes.")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.company_or_property or self.name

class LiftProject(TimeStampedModel):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
        ("maintenance", "Maintenance"),
    ]
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="lift_projects")
    title = models.CharField(max_length=180)
    lift_type = models.CharField(max_length=120, help_text="e.g. Passenger Lift, Home Lift, Goods Lift")
    location = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    expected_completion_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    image_2 = models.ImageField(upload_to="projects/", blank=True, null=True)
    show_on_website = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.title

class Enquiry(TimeStampedModel):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("in_progress", "In progress"),
        ("closed", "Closed"),
    ]
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    lift_interest = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    privacy_consent = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at:%d %b %Y}"


class Service(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True, help_text="Detailed service content; line breaks are preserved.")
    icon = models.CharField(max_length=32, default="arrow-up-right", help_text="Lucide-style icon name or short symbol")
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    cta_text = models.CharField(max_length=80, blank=True)
    cta_url = models.CharField(max_length=240, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    customer_name = models.CharField(max_length=120)
    role_or_location = models.CharField(max_length=160, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "customer_name"]

    def __str__(self):
        return self.customer_name


class HomeSection(TimeStampedModel):
    SECTION_CHOICES = [
        ("trust", "Trust / benefits strip"),
        ("categories", "Lift categories"),
        ("projects", "Featured projects"),
        ("products", "Featured products"),
        ("services", "Services"),
        ("testimonials", "Testimonials"),
        ("cta", "Quote call-to-action"),
    ]
    key = models.CharField(max_length=32, choices=SECTION_CHOICES, unique=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Homepage section visibility"
        verbose_name_plural = "Homepage section visibility"
    def __str__(self):
        return self.get_key_display()


class CustomSection(TimeStampedModel):
    title = models.CharField(max_length=180)
    eyebrow = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="custom-sections/", blank=True, null=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.CharField(max_length=240, blank=True)
    background_color = models.CharField(max_length=7, default="#f7f8fa", help_text="Section background hex colour")
    text_color = models.CharField(max_length=7, default="#101a2a", help_text="Section text hex colour")
    accent_color = models.CharField(max_length=7, default="#d5a12b", help_text="Section accent hex colour")
    font_family = models.CharField(max_length=20, choices=[("Manrope", "Manrope"), ("DM Sans", "DM Sans"), ("Montserrat", "Montserrat")], default="Manrope")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["display_order", "id"]
    def __str__(self):
        return self.title


class HeroSection(TimeStampedModel):
    PAGE_CHOICES = [("home", "Home"), ("about", "About"), ("services", "Services"), ("projects", "Our Work"), ("catalog", "Our Lifts"), ("contact", "Contact")]
    page_key = models.CharField(max_length=24, choices=PAGE_CHOICES, unique=True)
    eyebrow = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=220, blank=True)
    subtitle = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="page-heroes/", blank=True, null=True)
    cta_text = models.CharField(max_length=80, blank=True)
    cta_url = models.CharField(max_length=240, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ["page_key"]
    def __str__(self):
        return f"{self.get_page_key_display()} hero"

class AboutSection(TimeStampedModel):
    SECTION_CHOICES = [("introduction", "Company Introduction"), ("story", "Our Story"), ("mission", "Mission"), ("vision", "Vision"), ("values", "Core Values"), ("statistics", "Company Statistics"), ("image", "Section Image")]
    title = models.CharField(max_length=180)
    section_type = models.CharField(max_length=24, choices=SECTION_CHOICES, default="introduction")
    eyebrow = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="about/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["display_order", "id"]
    def __str__(self):
        return self.title

class CompanyStatistic(TimeStampedModel):
    value = models.CharField(max_length=40, blank=True, help_text="Example: 500")
    suffix = models.CharField(max_length=12, blank=True, default="+", help_text="Example: +")
    label = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    animate_count = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["display_order", "id"]
    def __str__(self):
        return f"{self.value}{self.suffix} — {self.label}"

class SocialLink(TimeStampedModel):
    PLATFORM_CHOICES = [("instagram", "Instagram"), ("facebook", "Facebook"), ("linkedin", "LinkedIn"), ("youtube", "YouTube"), ("x", "X / Twitter"), ("pinterest", "Pinterest")]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["display_order", "platform"]
    def __str__(self):
        return self.get_platform_display()
