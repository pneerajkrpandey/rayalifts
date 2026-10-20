from django.contrib import admin
from .models import SiteSettings, Page, Category, Product, Client, LiftProject, Enquiry, Service, Testimonial, HomeSection, CustomSection

admin.site.site_header = "Raya Lifts Website Administration"
admin.site.site_title = "Raya Lifts Admin"
admin.site.index_title = "Manage your website content"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand", {"fields": ("company_name", "tagline", "logo", "favicon")}),
        ("Design theme", {"fields": ("theme_navy", "theme_gold", "theme_surface", "theme_text", "theme_font"), "description": "Change the main site palette and typography without editing code."}),
        ("Contact", {"fields": ("phone", "whatsapp_number", "email", "contact_email", "address")}),
        ("Homepage", {"fields": ("hero_title", "hero_subtitle", "hero_image", "hero_image_2", "hero_image_3", "primary_cta_text", "primary_cta_url", "about_heading", "about_text", "experience_label")}),
        ("Header and footer controls", {"fields": ("show_header", "show_footer", "show_whatsapp_button", "footer_text")}),
        ("Social links", {"fields": ("facebook_url", "instagram_url", "linkedin_url", "youtube_url")}),
    )
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "show_in_navigation", "display_order", "updated_at")
    list_editable = ("is_active", "show_in_navigation", "display_order")
    list_filter = ("is_active", "show_in_navigation")
    search_fields = ("title", "intro", "body")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("display_order", "title")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "display_order", "updated_at")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ("name", "is_active", "display_order", "is_featured")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_featured", "is_active", "display_order", "updated_at")
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name", "summary", "description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company_or_property", "location", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "company_or_property", "location", "private_phone", "private_email")
    fields = ("name", "company_or_property", "location", "private_phone", "private_email", "internal_notes", "is_active")

@admin.register(LiftProject)
class LiftProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "lift_type", "status", "start_date", "completion_date", "show_on_website", "is_active", "display_order")
    list_editable = ("status", "show_on_website", "is_active", "display_order")
    list_filter = ("status", "lift_type", "show_on_website", "is_active")
    search_fields = ("title", "client__name", "client__company_or_property", "lift_type", "location")
    autocomplete_fields = ("client",)
    date_hierarchy = "start_date"

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "lift_interest", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "created_at", "lift_interest")
    search_fields = ("name", "phone", "email", "city", "message")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "display_order", "updated_at")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("title", "summary", "description")
    fieldsets = (("Service", {"fields": ("title", "slug", "summary", "description", "icon", "image")}), ("Call to action", {"fields": ("cta_text", "cta_url")}), ("Publishing", {"fields": ("is_active", "display_order")}))
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "role_or_location", "rating", "is_active", "display_order")
    list_editable = ("rating", "is_active", "display_order")
    list_filter = ("is_active", "rating")
    search_fields = ("customer_name", "role_or_location", "quote")


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ("get_key_display", "is_active", "display_order", "updated_at")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    ordering = ("display_order", "id")

@admin.register(CustomSection)
class CustomSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "display_order", "updated_at")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("title", "eyebrow", "body")
    ordering = ("display_order", "id")

# Page-level content controls. These models keep editorial updates out of templates.
from .models import HeroSection, AboutSection, CompanyStatistic, SocialLink

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("page_key", "title", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("page_key", "is_active")
    search_fields = ("title", "subtitle", "eyebrow")

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "section_type", "is_active", "display_order", "updated_at")
    list_editable = ("is_active", "display_order")
    list_filter = ("section_type", "is_active")
    search_fields = ("title", "eyebrow", "content")
    ordering = ("display_order", "id")

@admin.register(CompanyStatistic)
class CompanyStatisticAdmin(admin.ModelAdmin):
    list_display = ("value", "suffix", "label", "is_active", "display_order", "animate_count")
    list_editable = ("is_active", "display_order", "animate_count")
    list_filter = ("is_active", "animate_count")
    search_fields = ("value", "label")
    ordering = ("display_order", "id")

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "is_active", "display_order")
    list_editable = ("url", "is_active", "display_order")
    list_filter = ("platform", "is_active")
    ordering = ("display_order", "platform")
